import hashlib
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('sign_jar_natives', Path(__file__).parents[1] / 'sign-jar-natives.py')
signing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(signing)


class JarSigningTests(unittest.TestCase):
    def test_shell_signer_arguments_with_and_without_core_override(self):
        script = (Path(__file__).parents[1] / 'sign-macos-candidate.sh').read_text()
        arguments = script.split('signer_args=', 1)[1].split('"$JAVA_HOME/bin/jpackage"', 1)[0]
        prefix = '''script_dir='/tmp/tools path'
scratch='/tmp/candidate path'
MAC_SIGN_ID='Test Publisher (TEAM)'
unset PC110_NATIVE_LIBRARY
if [[ -n "$1" ]]; then PC110_NATIVE_LIBRARY=$1; fi
python3() { printf '%s\\n' "$@"; }
'''
        expected = ['/tmp/tools path/sign-jar-natives.py',
                    '/tmp/candidate path/image/PC110 Atlas.app/Contents/app',
                    '--identity', 'Developer ID Application: Test Publisher (TEAM)']
        for override in ('', '/tmp/rebuilt core.dylib'):
            result = subprocess.check_output(
                ['bash', '-uc', prefix + 'signer_args=' + arguments, 'signer-test', override],
                text=True).splitlines()
            self.assertEqual(result, expected + (['--pc110-native-library', override] if override else []))

    def test_qemu_executable_and_private_libraries_refresh_integrity_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            jar = Path(directory) / 'app.jar'
            prefix = 'qemu/macos-arm64/'
            files = {'qemu-system-i386': b'executable', 'lib/libglib.dylib': b'glib',
                     'data/atlas-demo.img': b'demo'}
            with zipfile.ZipFile(jar, 'w') as archive:
                for name, data in files.items():
                    archive.writestr(prefix + name + ('.bin' if name.endswith('.dylib') else ''), data)
                archive.writestr(prefix + 'files.sha256', ''.join(
                    f'{hashlib.sha256(data).hexdigest()}  {name}\n' for name, data in files.items()))
            self.assertEqual(signing.sign_jar(jar, lambda data: data + b'-signed'), 2)
            with zipfile.ZipFile(jar) as archive:
                self.assertEqual(archive.read(prefix + 'qemu-system-i386'), b'executable-signed')
                for line in archive.read(prefix + 'files.sha256').decode().splitlines():
                    digest, name = line.split('  ', 1)
                    entry = prefix + name + ('.bin' if name.endswith('.dylib') else '')
                    self.assertEqual(digest, hashlib.sha256(archive.read(entry)).hexdigest())

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
