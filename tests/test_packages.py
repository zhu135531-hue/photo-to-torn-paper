import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('packages', ROOT/'scripts/build_packages.py')
packages = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packages)


class PackageTests(unittest.TestCase):
    def test_distributions_have_real_local_entrypoints_and_no_user_images(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            packages.build(output)
            for filename in ('torn-paper.zip', 'cursor-plugin.zip', 'photo-studio.zip', 'torn-paper-portable.zip', 'torn-paper-trae.zip'):
                with zipfile.ZipFile(output/filename) as archive:
                    names = archive.namelist()
                    self.assertEqual(len(names), len(set(names)))
                    for name in names:
                        self.assertNotIn('..', Path(name).parts)
                        self.assertFalse(Path(name).is_absolute())
                        self.assertNotIn(Path(name).suffix.lower(), ('.jpg', '.png', '.webp', '.env', '.pyc'))
                    for name in names:
                        if '/rules/' in name:
                            rule = archive.read(name).decode()
                            target = rule.split('Load `', 1)[1].split('`', 1)[0]
                            package_root = name.split('/', 1)[0]
                            self.assertIn(package_root+'/'+target, names)
                            self.assertIn('alwaysApply: true', rule)
            with zipfile.ZipFile(output/'torn-paper-trae.zip') as archive:
                self.assertIn('SKILL.md', archive.namelist())

    def test_portable_import_needs_no_missing_files(self):
        text = packages.standalone()
        self.assertNotIn('`references/', text)
        for content in ('COLOR LOCK', 'The person is one intact sheet', 'Host execution routes', 'Waterline'):
            self.assertIn(content, text)

    def test_reproducible_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory)/'a', Path(directory)/'b'
            packages.build(first)
            packages.build(second)
            for path in first.iterdir():
                self.assertEqual(hashlib.sha256(path.read_bytes()).digest(),
                                 hashlib.sha256((second/path.name).read_bytes()).digest())
            with self.assertRaises(FileExistsError):
                packages.build(first)


if __name__ == '__main__':
    unittest.main()
