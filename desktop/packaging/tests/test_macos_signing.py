import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('sign_jar_natives', Path(__file__).parents[1] / 'sign-jar-natives.py')
signing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(signing)


class JarSigningTests(unittest.TestCase):
    def test_nested_and_other_architecture_libraries_and_cache_hashes(self):
        with tempfile.TemporaryDirectory() as directory:
            jar = Path(directory) / 'app.jar'
            entries = {
                'native/libpc110_desktop.dylib': b'core',
                'libskiko-macos-arm64.dylib': b'arm64',
                'libskiko-macos-x64.dylib': b'x64',
                'libskiko-macos-x64.dylib.sha256': b'old',
                'META-INF/MANIFEST.MF': b'Manifest-Version: 1.0\n',
                'some/Class.class': b'unchanged',
            }
            with zipfile.ZipFile(jar, 'w', zipfile.ZIP_DEFLATED) as archive:
                archive.comment = b'preserved'
                for name, data in entries.items():
                    archive.writestr(name, data)
            self.assertEqual(signing.sign_jar(jar, lambda data: data + b'-signed'), 3)
            with zipfile.ZipFile(jar) as archive:
                self.assertEqual(archive.comment, b'preserved')
                self.assertEqual(set(archive.namelist()), set(entries))
                self.assertEqual(archive.read('native/libpc110_desktop.dylib'), b'core-signed')
                self.assertEqual(archive.read('libskiko-macos-arm64.dylib'), b'arm64-signed')
                self.assertEqual(archive.read('libskiko-macos-x64.dylib.sha256'),
                                 hashlib.sha256(b'x64-signed').hexdigest().encode())
                self.assertEqual(archive.read('some/Class.class'), b'unchanged')

    def test_no_native_library_is_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            jar = Path(directory) / 'app.jar'
            with zipfile.ZipFile(jar, 'w') as archive:
                archive.writestr('some/Class.class', b'original')
            before = jar.read_bytes()
            self.assertEqual(signing.sign_jar(jar, lambda data: self.fail('Unexpected signer')), 0)
            self.assertEqual(jar.read_bytes(), before)

    def test_replacement_core_is_signed_without_changing_other_libraries(self):
        with tempfile.TemporaryDirectory() as directory:
            jar = Path(directory) / 'app.jar'
            with zipfile.ZipFile(jar, 'w') as archive:
                archive.writestr('native/libpc110_desktop.dylib', b'old-core')
                archive.writestr('graphics.dylib', b'graphics')
            signing.sign_jar(jar, lambda data: data + b'-signed',
                             {'native/libpc110_desktop.dylib': b'macos12-core'})
            with zipfile.ZipFile(jar) as archive:
                self.assertEqual(archive.read('native/libpc110_desktop.dylib'), b'macos12-core-signed')
                self.assertEqual(archive.read('graphics.dylib'), b'graphics-signed')

    def test_signed_archive_is_not_silently_invalidated(self):
        with tempfile.TemporaryDirectory() as directory:
            jar = Path(directory) / 'app.jar'
            with zipfile.ZipFile(jar, 'w') as archive:
                archive.writestr('library.dylib', b'original')
                archive.writestr('META-INF/VENDOR.SF', b'signature')
            before = jar.read_bytes()
            with self.assertRaisesRegex(ValueError, 'Java archive signature'):
                signing.sign_jar(jar, lambda data: data)
            self.assertEqual(jar.read_bytes(), before)

    def test_signer_failure_preserves_original_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            jar = Path(directory) / 'app.jar'
            with zipfile.ZipFile(jar, 'w') as archive:
                archive.writestr('library.dylib', b'original')
            before = jar.read_bytes()
            def fail(_):
                raise RuntimeError('Signing failed')
            with self.assertRaisesRegex(RuntimeError, 'Signing failed'):
                signing.sign_jar(jar, fail)
            self.assertEqual(jar.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
