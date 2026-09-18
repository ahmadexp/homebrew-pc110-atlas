import hashlib
import importlib.util
import os
import re
import shutil
import stat
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

PACKAGING = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('pi_apps', PACKAGING / 'package-pi-apps.py')
pi_apps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pi_apps)


class PiAppsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='pc110-pi-apps-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.app = self.root / 'PC110 Atlas'
        shutil.copytree(pi_apps.APP, self.app)
        self.version = re.search(r'^version=([0-9.]+)$',
                                 (self.app / 'install-64').read_text(), re.M)[1]
        self.deb = self.root / f'pc110-atlas-{self.version}-linux-arm64.deb'
        self.deb.write_bytes(b'disposable package fixture, not a real installer')
        self.sha = hashlib.sha256(self.deb.read_bytes()).hexdigest()
        script = self.app / 'install-64'
        script.write_text(re.sub(r'^sha256=[0-9a-f]{64}$', f'sha256={self.sha}',
                                 script.read_text(), flags=re.M))
        self.downloads = self.root / 'downloads'
        self.downloads.mkdir()

    def run_script(self, name='install-64', codename='trixie', arch='64', fail='', tail=''):
        # Mock network/package mutations, but use the real SHA-256 checker and shell.
        helpers = r'''
error() { printf '%s\n' "$*" >&2; exit 1; }
wget() {
  printf 'download %s\n' "$3" >> "$CALLS"
  [ "$1" = '-O' ] || return 7
  [ "$FAIL" != download ] || return 9
  cp "$FIXTURE" "$2"
  [ "$FAIL" != tamper ] || printf 'tampered' >> "$2"
  return 0
}
install_packages() {
  test -s "$1" || return 8
  printf 'install\n' >> "$CALLS"
  [ "$FAIL" != install ]
}
purge_packages() { printf 'purge\n' >> "$CALLS"; [ "$FAIL" != purge ]; }
source "$SCRIPT"
'''
        env = dict(os.environ, arch=arch, __os_codename=codename, FAIL=fail,
                   FIXTURE=str(self.deb), CALLS=str(self.root / 'calls'),
                   SCRIPT=str(self.app / name), TMPDIR=str(self.downloads))
        result = subprocess.run(['bash', '-c', helpers + tail], env=env,
                                text=True, capture_output=True, timeout=15)
        calls = self.root / 'calls'
        return result, calls.read_text() if calls.exists() else ''

    def test_accepted_systems_verify_bytes_and_use_dependency_helper(self):
        for codename in ('bookworm', 'trixie', 'jammy', 'noble', 'resolute'):
            with self.subTest(codename=codename):
                result, calls = self.run_script(codename=codename)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(f'desktop-v{self.version}/pc110-atlas-{self.version}-linux-arm64.deb', calls)
                self.assertIn('install\n', calls)
                self.assertEqual(list(self.downloads.iterdir()), [])

    def test_unsupported_systems_fail_before_downloading(self):
        for codename in ('buster', 'focal', 'bullseye', '', 'unknown'):
            with self.subTest(codename=codename):
                result, calls = self.run_script(codename=codename)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(calls, '')
        result, calls = self.run_script(arch='32')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(calls, '')

    def test_download_and_checksum_failure_cannot_install_and_leave_no_temp_files(self):
        for fail in ('download', 'tamper'):
            with self.subTest(fail=fail):
                result, calls = self.run_script(fail=fail)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('install\n', calls)
                self.assertEqual(list(self.downloads.iterdir()), [])

    def test_installer_failure_propagates_and_cleans_up(self):
        result, calls = self.run_script(fail='install')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('install\n', calls)
        self.assertEqual(list(self.downloads.iterdir()), [])

    def test_download_trap_does_not_leak_into_calling_shell(self):
        result, _ = self.run_script(tail="test -z \"$(trap -p EXIT)\"\n")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_uninstall_only_uses_pi_apps_dependency_accounting(self):
        result, calls = self.run_script(name='uninstall')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, 'purge\n')
        result, _ = self.run_script(name='uninstall', fail='purge')
        self.assertNotEqual(result.returncode, 0)
        text = (self.app / 'uninstall').read_text()
        self.assertNotRegex(text, r'\b(rm|apt|apt-get|dpkg)\b')

    def test_zip_is_deterministic_allowlisted_and_keeps_script_modes(self):
        (self.app / 'private.img').write_bytes(b'never distribute')
        outputs = [self.root / f'candidate-{index}.zip' for index in range(2)]
        for output in outputs:
            pi_apps.package(self.deb, output, self.app)
        self.assertEqual(outputs[0].read_bytes(), outputs[1].read_bytes())
        with zipfile.ZipFile(outputs[0]) as archive:
            self.assertEqual(archive.namelist(), [f'PC110 Atlas/{name}' for name in pi_apps.FILES])
            for name in ('install-64', 'uninstall'):
                self.assertEqual(stat.S_IMODE(archive.getinfo(f'PC110 Atlas/{name}').external_attr >> 16), 0o775)
            self.assertNotIn('PC110 Atlas/install-32', archive.namelist())

    def test_zip_refuses_overwrite_and_wrong_deb_before_writing(self):
        output = self.root / 'candidate.zip'
        pi_apps.package(self.deb, output, self.app)
        with self.assertRaises(FileExistsError):
            pi_apps.package(self.deb, output, self.app)
        self.deb.write_bytes(b'wrong version')
        with self.assertRaises(ValueError):
            pi_apps.package(self.deb, self.root / 'invalid.zip', self.app)
        self.assertFalse((self.root / 'invalid.zip').exists())

    def test_zip_rejects_missing_and_symlinked_metadata_and_wrong_icons(self):
        credits = self.app / 'credits'
        credits.unlink()
        for linked in (False, True):
            if linked:
                credits.symlink_to(self.deb)
            with self.assertRaises(ValueError):
                pi_apps.package(self.deb, self.root / 'invalid.zip', self.app)
        credits.unlink()
        credits.write_text('Ahmad Byagowi\n')
        shutil.copyfile(self.app / 'icon-24.png', self.app / 'icon-64.png')
        with self.assertRaises(ValueError):
            pi_apps.package(self.deb, self.root / 'invalid.zip', self.app)


if __name__ == '__main__':
    unittest.main()
