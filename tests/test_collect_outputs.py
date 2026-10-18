"""Security regressions use synthetic fixtures, never personal photos."""
import contextlib
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('collector', ROOT/'skills/torn-paper/scripts/collect_outputs.py')
collector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collector)


class CollectorSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.workspace = self.root/'workspace'
        self.sources = self.root/'sources'
        self.generated = self.root/'generated'
        for folder in (self.workspace, self.sources, self.generated):
            folder.mkdir()
        self.source = self.sources/'source.png'
        self.image = self.generated/'generated.png'
        Image.new('RGB', (8, 8), 'red').save(self.source)
        Image.new('RGB', (8, 8), 'blue').save(self.image)
        self.manifest = self.root/'manifest.json'
        self.output = self.workspace/'run'
        self.data = {'execution': {'route': 'synthetic test', 'private_field': 'PRIVATE_EXECUTION'},
                     'images': [{'id': 'test-whole', 'scene': 'test', 'event': 'whole',
                       'source_path': str(self.source), 'generated_path': str(self.image),
                       'prompt': 'PRIVATE_PROMPT',
                       'review': {'status': 'accepted', 'notes': 'PRIVATE_NOTES', 'key': 'PRIVATE_FIELD'},
                       'correction': {'reason': 'reason', 'initial_prompt': 'PRIVATE_ORIGINAL',
                                      'attempts': 2, 'key': 'PRIVATE_CORRECTION'}}]}

    def run_collect(self, **kwargs):
        self.manifest.write_text(json.dumps(self.data), encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            collector.collect(self.manifest, self.output, source_roots=[self.sources],
                              generated_roots=[self.generated], workspace_root=self.workspace, **kwargs)

    def test_valid_output_is_byte_identical(self):
        self.run_collect()
        self.assertEqual((self.output/'test-whole.png').read_bytes(), self.image.read_bytes())
        self.assertEqual(len(list(self.output.iterdir())), 2)

    def test_default_log_omits_private_text_and_source_fingerprint(self):
        self.run_collect()
        saved = (self.output/'run.json').read_text(encoding='utf-8')
        self.assertNotIn('PRIVATE_', saved)
        self.assertNotIn(str(self.source), saved)
        self.assertNotIn('source_sha256', saved)

    def test_verbose_log_is_opt_in_and_drops_unknown_fields(self):
        self.run_collect(include_prompts=True)
        saved = (self.output/'run.json').read_text(encoding='utf-8')
        self.assertIn('PRIVATE_PROMPT', saved)
        self.assertNotIn('PRIVATE_FIELD', saved)
        self.assertNotIn('PRIVATE_CORRECTION', saved)
        self.assertNotIn('PRIVATE_EXECUTION', saved)

    def test_generated_path_escape_rejected(self):
        other = self.root/'outside.png'
        other.write_bytes(self.image.read_bytes())
        self.data['images'][0]['generated_path'] = str(other)
        with self.assertRaisesRegex(ValueError, 'outside caller-authorized'):
            self.run_collect()
        self.assertFalse(self.output.exists())

    def test_source_path_escape_rejected(self):
        self.data['images'][0]['source_path'] = str(self.image)
        with self.assertRaisesRegex(ValueError, 'outside caller-authorized'):
            self.run_collect()

    def test_output_workspace_escape_rejected(self):
        self.output = self.root/'outside-output'
        with self.assertRaisesRegex(ValueError, 'authorized workspace'):
            self.run_collect()

    def test_protected_configuration_directory_rejected(self):
        self.output = self.workspace/'.git'/'new-run'
        with self.assertRaisesRegex(ValueError, 'protected'):
            self.run_collect()

    def test_existing_output_is_never_overwritten(self):
        self.output.mkdir()
        marker = self.output/'keep.txt'
        marker.write_text('keep', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'never overwritten'):
            self.run_collect()
        self.assertEqual(marker.read_text(), 'keep')

    def test_traversal_image_id_rejected(self):
        self.data['images'][0]['id'] = '../escape'
        with self.assertRaises(ValueError):
            self.run_collect()

    def test_duplicate_id_rejected_before_any_output(self):
        self.data['images'].append(copy.deepcopy(self.data['images'][0]))
        with self.assertRaisesRegex(ValueError, 'unique'):
            self.run_collect()
        self.assertFalse(self.output.exists())

    def test_unchanged_source_is_not_an_output(self):
        self.image.write_bytes(self.source.read_bytes())
        with self.assertRaisesRegex(ValueError, 'unchanged'):
            self.run_collect()

    def test_ratio_mismatch_rejected(self):
        Image.new('RGB', (16, 8), 'blue').save(self.image)
        with self.assertRaisesRegex(ValueError, 'Aspect ratio'):
            self.run_collect()

    def test_pixel_limit_checked_before_decode(self):
        with patch.object(collector, 'MAX_PIXELS', 32):
            with self.assertRaisesRegex(ValueError, 'pixel limit'):
                self.run_collect()

    def test_encoded_file_limit(self):
        with patch.object(collector, 'MAX_FILE_BYTES', 16):
            with self.assertRaisesRegex(ValueError, 'size limit'):
                self.run_collect()

    def test_total_byte_limit(self):
        with patch.object(collector, 'MAX_TOTAL_BYTES', 1):
            with self.assertRaisesRegex(ValueError, 'total input-byte limit'):
                self.run_collect()

    def test_manifest_size_limit(self):
        with patch.object(collector, 'MAX_MANIFEST_BYTES', 10):
            with self.assertRaisesRegex(ValueError, 'size limit'):
                self.run_collect()

    def test_batch_count_limit(self):
        self.data['images'] *= collector.MAX_IMAGES + 1
        with self.assertRaisesRegex(ValueError, 'Manifest needs'):
            self.run_collect()

    def test_unsupported_format_not_opened(self):
        Image.new('RGB', (8, 8), 'green').save(self.image, format='TIFF')
        with self.assertRaises((ValueError, OSError)):
            self.run_collect()

    def test_animation_rejected(self):
        frames = [Image.new('RGB', (8, 8), color) for color in ('blue', 'green')]
        frames[0].save(self.image, format='PNG', save_all=True, append_images=frames[1:])
        with self.assertRaisesRegex(ValueError, 'single-frame'):
            self.run_collect()

    def test_unreviewed_output_rejected(self):
        self.data['images'][0]['review']['status'] = 'rejected'
        with self.assertRaisesRegex(ValueError, 'accepted visual review'):
            self.run_collect()

    def test_generated_gps_metadata_rejected(self):
        exif = Image.Exif()
        exif[34853] = {1: 'N', 2: (1.0, 2.0, 3.0)}
        Image.new('RGB', (8, 8), 'blue').save(self.image, format='PNG', exif=exif)
        with self.assertRaisesRegex(ValueError, 'GPS metadata'):
            self.run_collect()

    def test_validated_byte_snapshot_is_written(self):
        original = self.image.read_bytes()
        inspect = collector.inspect_image
        def changed_after_validation(data, generated=False):
            result = inspect(data, generated=generated)
            if generated:
                Image.new('RGB', (8, 8), 'green').save(self.image)
            return result
        with patch.object(collector, 'inspect_image', side_effect=changed_after_validation):
            self.run_collect()
        self.assertEqual((self.output/'test-whole.png').read_bytes(), original)
        self.assertNotEqual(self.image.read_bytes(), original)

    def test_relative_path_rejected(self):
        self.data['images'][0]['generated_path'] = 'generated.png'
        with self.assertRaisesRegex(ValueError, 'absolute local'):
            self.run_collect()

    def test_unc_path_rejected(self):
        self.data['images'][0]['generated_path'] = '//server/share/private.png'
        with self.assertRaisesRegex(ValueError, 'network shares'):
            self.run_collect()


if __name__ == '__main__':
    unittest.main()
