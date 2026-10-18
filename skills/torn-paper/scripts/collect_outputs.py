"""Collect reviewed images within caller-supplied local path boundaries.

Requires Python 3.11+ and Pillow>=13.0.0,<14. No network, command execution,
generation, resizing, or automatic installation. Prompts are opt-in private logs.
"""
import argparse
import hashlib
import io
import json
import os
import re
import stat
import warnings
from pathlib import Path

from PIL import Image
from PIL import __version__ as PILLOW_VERSION

# Pillow 13.0.0 fixes JPEG decoder and Exif vulnerabilities relevant to photos.
if tuple(int(p) for p in PILLOW_VERSION.split('.')[:3]) < (13, 0, 0):
    raise RuntimeError('This collector requires Pillow>=13.0.0; update it in an isolated environment')

EVENTS = {'whole', 'window', 'stop', 'sides', 'stack', 'waterline', 'through', 'sky', 'frame'}
MAX_FILE_BYTES = 32 * 1024 * 1024
MAX_TOTAL_BYTES = 256 * 1024 * 1024
MAX_MANIFEST_BYTES = 2 * 1024 * 1024
MAX_IMAGES = 32
MAX_PIXELS = 40_000_000
MAX_TEXT = 32_768
FORMATS = {'PNG': '.png', 'JPEG': '.jpg', 'WEBP': '.webp'}
PROTECTED = {'.git', '.agents', '.codex', '.github', '.aws'}
EXECUTION_KEYS = {'date', 'route', 'tool', 'model', 'invocation', 'initial_generations', 'corrections'}


def text(value, label, maximum=MAX_TEXT):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f'Invalid or oversized {label}')
    return value


def local_path(value):
    path = Path(value)
    if not path.is_absolute() or str(path).replace('\\', '/').startswith('//'):
        raise ValueError('Paths must be absolute local paths; network shares are not supported')
    # OneDrive placeholders are not symlinks. Reject actual links/junctions only.
    for part in (path, *path.parents):
        if part.is_symlink() or getattr(os.path, 'isjunction', lambda p: False)(part):
            raise ValueError('Symbolic links and junctions are not supported')
    return path.resolve()


def beneath(path, roots):
    return any(path.is_relative_to(root) for root in roots)


def read_regular(path, limit):
    if not path.is_file():
        raise ValueError('Input must be a regular local file')
    with path.open('rb') as file:
        info = os.fstat(file.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise ValueError('Input file exceeds the size limit or is not regular')
        data = file.read(limit + 1)
    if len(data) > limit:
        raise ValueError('Input file exceeds the size limit')
    return data


def inspect_image(data, generated=False):
    with warnings.catch_warnings():
        warnings.simplefilter('error', Image.DecompressionBombWarning)
        with Image.open(io.BytesIO(data), formats=tuple(FORMATS)) as image:
            if image.format not in FORMATS or getattr(image, 'n_frames', 1) != 1:
                raise ValueError('Only single-frame PNG, JPEG and WEBP images are supported')
            width, height = image.size
            if width * height > MAX_PIXELS:
                raise ValueError('Image exceeds the decoded pixel limit')
            exif = image.getexif()
            if generated and exif.get(34853):
                raise ValueError('Generated image contains GPS metadata; inspect it before copying')
            if exif.get(274) in {5, 6, 7, 8}:
                width, height = height, width
            image.load()
            return (width, height), image.format


def clean_metadata(entry, include_prompts):
    # Unknown fields are never serialized to the result, even when verbose.
    review = entry.get('review')
    if not isinstance(review, dict) or review.get('status') != 'accepted':
        raise ValueError('Every image must have an explicit accepted visual review')
    notes = text(review.get('notes'), 'review notes')
    prompt = text(entry.get('prompt'), 'prompt')
    result = {'review': {'status': 'accepted'}}
    if include_prompts:
        result['prompt'] = prompt
        result['review']['notes'] = notes
        correction = entry.get('correction')
        if correction is not None:
            if not isinstance(correction, dict):
                raise ValueError('Correction must be an object')
            result['correction'] = {}
            for key in ('reason', 'initial_prompt'):
                if key in correction:
                    result['correction'][key] = text(correction[key], 'correction ' + key)
            if 'attempts' in correction:
                if type(correction['attempts']) is not int or not 1 <= correction['attempts'] <= 100:
                    raise ValueError('Invalid correction attempts')
                result['correction']['attempts'] = correction['attempts']
    return result


def collect(manifest_path, output_dir, *, source_roots, generated_roots,
            workspace_root, include_prompts=False):
    source_roots = [local_path(root) for root in source_roots]
    generated_roots = [local_path(root) for root in generated_roots]
    workspace_root = local_path(workspace_root)
    if not source_roots or not generated_roots or any(not p.is_dir() for p in source_roots + generated_roots):
        raise ValueError('Caller must supply existing source and generated-image directories')
    if not workspace_root.is_dir():
        raise ValueError('Workspace root must be an existing directory')
    output_dir = local_path(output_dir)
    if not beneath(output_dir, [workspace_root]) or output_dir == workspace_root:
        raise ValueError('Output directory must be a new child of the authorized workspace')
    if PROTECTED.intersection(output_dir.relative_to(workspace_root).parts):
        raise ValueError('Output cannot be placed in a protected configuration directory')
    if output_dir.exists():
        raise ValueError('Use a new output directory; existing runs are never overwritten')
    manifest = json.loads(read_regular(local_path(manifest_path), MAX_MANIFEST_BYTES).decode('utf-8-sig'))
    if not isinstance(manifest, dict):
        raise ValueError('Manifest must be an object')
    entries = manifest.get('images')
    if not isinstance(entries, list) or not 1 <= len(entries) <= MAX_IMAGES:
        raise ValueError(f'Manifest needs 1 to {MAX_IMAGES} images')

    execution = manifest.get('execution', {})
    if not isinstance(execution, dict):
        raise ValueError('Execution must be an object')
    clean_execution = {}
    for key in EXECUTION_KEYS.intersection(execution):
        value = execution[key]
        if key in {'initial_generations', 'corrections'}:
            if type(value) is not int or not 0 <= value <= 10_000:
                raise ValueError('Invalid execution counter')
        else:
            value = text(value, 'execution ' + key, 1024)
        clean_execution[key] = value

    planned, seen, source_cache, total_bytes = [], set(), {}, 0
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('Image entry must be an object')
        identifier = text(entry.get('id'), 'image ID', 100)
        scene = text(entry.get('scene'), 'scene', 100)
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', identifier) or identifier in seen:
            raise ValueError('Image IDs must be unique safe lowercase names')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', scene):
            raise ValueError('Scene must be a safe lowercase name')
        seen.add(identifier)
        if entry.get('event') not in EVENTS:
            raise ValueError('Unknown tear event')
        metadata = clean_metadata(entry, include_prompts)
        source = local_path(text(entry.get('source_path'), 'source path', 4096))
        generated = local_path(text(entry.get('generated_path'), 'generated path', 4096))
        if not beneath(source, source_roots) or not beneath(generated, generated_roots):
            raise ValueError('Input path is outside caller-authorized directories')
        if source == generated:
            raise ValueError('A source photograph cannot be the generated deliverable')
        if source not in source_cache:
            source_data = read_regular(source, MAX_FILE_BYTES)
            total_bytes += len(source_data)
            if total_bytes > MAX_TOTAL_BYTES:
                raise ValueError('Batch exceeds the total input-byte limit')
            source_size, _ = inspect_image(source_data)
            source_cache[source] = (source_size, hashlib.sha256(source_data).hexdigest())
            del source_data
        source_size, source_hash = source_cache[source]
        data = read_regular(generated, MAX_FILE_BYTES)
        total_bytes += len(data)
        if total_bytes > MAX_TOTAL_BYTES:
            raise ValueError('Batch exceeds the total input-byte limit')
        generated_size, image_format = inspect_image(data, generated=True)
        generated_hash = hashlib.sha256(data).hexdigest()
        if source_hash == generated_hash:
            raise ValueError('Source photo was returned unchanged')
        ratio_error = abs((generated_size[0] / generated_size[1]) /
                          (source_size[0] / source_size[1]) - 1)
        if ratio_error > 0.02:
            raise ValueError('Aspect ratio differs by more than 2%')
        filename = identifier + FORMATS[image_format]
        record = {'id': identifier, 'scene': scene, 'event': entry['event'],
                  'source_size': list(source_size), 'native_size': list(generated_size),
                  'file': filename, 'sha256': generated_hash, 'resized': False, **metadata}
        planned.append((data, filename, record))

    # Data is held as a bounded, verified snapshot: do not reread paths at copy time.
    output_dir.mkdir(parents=True, exist_ok=False)
    records = []
    for data, filename, record in planned:
        with (output_dir / filename).open('xb') as file:
            file.write(data)
        records.append(record)
    report = {'execution': clean_execution, 'images': records,
              'privacy': {'prompts_included': include_prompts,
                          'private_log_review_required': include_prompts},
              'validation': {'files': len(records), 'pixels_modified': False,
                             'aspect_ratio_tolerance': 0.02,
                             'visual_review': 'Supplied by caller, not inferred from file hashes'}}
    with (output_dir / 'run.json').open('x', encoding='utf-8') as file:
        json.dump(report, file, ensure_ascii=False, indent=2)
        file.write('\n')
    print(json.dumps({'saved': len(records), 'directory': str(output_dir),
                      'source_photos_copied': False, 'resized': False,
                      'prompts_included': include_prompts}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--source-root', action='append', required=True, type=Path)
    parser.add_argument('--generated-root', action='append', required=True, type=Path)
    parser.add_argument('--workspace-root', type=Path, default=Path.cwd())
    parser.add_argument('--include-prompts', action='store_true',
                        help='Write actual prompts and review text to a private local log')
    arguments = parser.parse_args()
    collect(arguments.manifest, arguments.output_dir, source_roots=arguments.source_root,
            generated_roots=arguments.generated_root, workspace_root=arguments.workspace_root,
            include_prompts=arguments.include_prompts)
