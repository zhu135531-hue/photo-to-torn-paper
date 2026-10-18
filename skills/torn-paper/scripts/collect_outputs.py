"""Verify and copy generated files without modifying their pixels.

Requires Pillow. Generation and visual review happen in the host image tool.
"""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

from PIL import Image, ImageOps

EVENTS = {'whole', 'window', 'stop', 'sides', 'stack', 'waterline', 'through', 'sky', 'frame'}


def dimensions(path):
    with Image.open(path) as image:
        image.load()
        return ImageOps.exif_transpose(image).size, image.format


def digest(path):
    with path.open('rb') as file:
        return hashlib.file_digest(file, 'sha256').hexdigest()


def collect(manifest_path, output_dir):
    manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    entries = manifest.get('images')
    if not isinstance(entries, list) or not entries:
        raise ValueError('Manifest needs a non-empty images list')
    if output_dir.exists():
        raise ValueError('Use a new output directory; existing runs are never overwritten')

    planned, seen = [], set()
    for entry in entries:
        identifier = entry['id']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', identifier) or identifier in seen:
            raise ValueError('Image IDs must be unique safe lowercase names')
        seen.add(identifier)
        if entry['event'] not in EVENTS:
            raise ValueError(f'Unknown tear event: {identifier}')
        if entry.get('review', {}).get('status') != 'accepted':
            raise ValueError(f'Visual review has not accepted: {identifier}')
        if not entry['review'].get('notes') or not entry.get('prompt'):
            raise ValueError(f'Missing actual prompt or review notes: {identifier}')
        source, generated = Path(entry['source_path']), Path(entry['generated_path'])
        if source.resolve() == generated.resolve():
            raise ValueError('A source photograph cannot be the generated deliverable')
        source_size, _ = dimensions(source)
        generated_size, image_format = dimensions(generated)
        if image_format not in {'PNG', 'JPEG', 'WEBP'}:
            raise ValueError(f'Unsupported generated format: {image_format}')
        if digest(source) == digest(generated):
            raise ValueError('Source photo was returned unchanged')
        relative_ratio_error = abs((generated_size[0] / generated_size[1]) /
                                   (source_size[0] / source_size[1]) - 1)
        if relative_ratio_error > 0.02:
            raise ValueError(f'Aspect ratio differs by more than 2%: {identifier}')
        extension = {'PNG': '.png', 'JPEG': '.jpg', 'WEBP': '.webp'}[image_format]
        filename = identifier + extension
        record = {
            'id': identifier, 'scene': entry['scene'], 'event': entry['event'],
            'source_size': list(source_size), 'source_sha256': digest(source),
            'native_size': list(generated_size), 'file': filename,
            'sha256': digest(generated), 'resized': False,
            'prompt': entry['prompt'], 'review': entry['review'],
        }
        if entry.get('correction'):
            record['correction'] = entry['correction']
        planned.append((generated, filename, record))

    output_dir.mkdir(parents=True, exist_ok=False)
    records = []
    for generated, filename, record in planned:
        destination = output_dir / filename
        shutil.copyfile(generated, destination)
        if digest(destination) != record['sha256']:
            raise RuntimeError(f'Copy verification failed: {filename}')
        records.append(record)
    report = {'execution': manifest.get('execution', {}), 'images': records,
              'validation': {'files': len(records), 'pixels_modified': False,
                             'aspect_ratio_tolerance': 0.02,
                             'visual_review': 'human/model observation, not inferred from hashes'}}
    (output_dir / 'run.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'saved': len(records), 'directory': str(output_dir),
                      'source_photos_copied': False, 'resized': False}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    arguments = parser.parse_args()
    collect(arguments.manifest, arguments.output_dir)
