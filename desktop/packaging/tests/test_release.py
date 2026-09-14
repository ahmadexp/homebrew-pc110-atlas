import argparse
import hashlib
import importlib.util
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


def module(name):
    path = Path(__file__).resolve().parents[1] / f'{name}.py'
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


release = module('prepare-release')
downloads = module('verify-downloads')


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.assets = self.root / 'assets'
        self.assets.mkdir()

    def artifacts(self):
        for suffix in ('windows-x64.msi', 'macos-x64.dmg', 'macos-arm64.dmg'):
            (self.assets / f'pc110-atlas-1.2.3-{suffix}').write_bytes(suffix.encode())

    def test_manifests_pin_architecture_specific_bytes(self):
        self.artifacts()
        output = self.root / 'manifests'
        release.manifests(self.assets, output, '1.2.3', 'owner/project')
        cask = (output / 'homebrew/Casks/pc110-atlas.rb').read_text()
        for arch in ('x64', 'arm64'):
            self.assertIn(hashlib.sha256(f'macos-{arch}.dmg'.encode()).hexdigest(), cask)
        install = (output / 'chocolatey/tools/chocolateyInstall.ps1').read_text()
        self.assertIn(hashlib.sha256(b'windows-x64.msi').hexdigest(), install)
        self.assertIn('desktop-v1.2.3/pc110-atlas-1.2.3-windows-x64.msi', install)
        ET.parse(output / 'chocolatey/pc110-atlas.nuspec')

    def test_missing_architecture_fails_before_writing_manifests(self):
        self.artifacts()
        (self.assets / 'pc110-atlas-1.2.3-macos-arm64.dmg').unlink()
        with self.assertRaises(ValueError):
            release.manifests(self.assets, self.root / 'output', '1.2.3', 'owner/project')
        self.assertFalse((self.root / 'output').exists())

    def test_chocolatey_can_release_without_macos_artifacts(self):
        (self.assets / 'pc110-atlas-1.2.3-windows-x64.msi').write_bytes(b'msi')
        output = self.root / 'manifests'
        release.manifests(self.assets, output, '1.2.3', 'owner/public-releases', 'chocolatey')
        install = (output / 'chocolatey/tools/chocolateyInstall.ps1').read_text()
        self.assertIn('https://github.com/owner/public-releases/releases/download/', install)
        self.assertFalse((output / 'homebrew').exists())
        package = ET.parse(output / 'chocolatey/pc110-atlas.nuspec')
        ns = {'n': 'http://schemas.microsoft.com/packaging/2015/06/nuspec.xsd'}
        self.assertEqual(package.find('.//n:licenseUrl', ns).text,
                         'https://github.com/owner/public-releases/blob/main/LICENSING.md')

    def test_detects_tampered_or_unlisted_release_file(self):
        self.artifacts()
        release.checksums(self.assets)
        downloads.verify(self.assets)
        artifact = self.assets / 'pc110-atlas-1.2.3-windows-x64.msi'
        artifact.write_bytes(b'changed')
        with self.assertRaises(ValueError):
            downloads.verify(self.assets)

    def test_rejects_ambiguous_old_builds(self):
        directory = self.root / 'build/dmg'
        directory.mkdir(parents=True)
        for version in ('1.0', '2.0'):
            (directory / f'Atlas-{version}.dmg').write_bytes(b'dmg')
        with self.assertRaises(ValueError):
            release.collect(directory.parent, self.assets, '1.2.3', 'macos', 'arm64')

    def test_rejects_invalid_versions_and_template_injection(self):
        for version in ('1.2.3-beta', '1.02.3', '256.1.0', '1.0.65536', '../1.0'):
            with self.assertRaises(argparse.ArgumentTypeError):
                release.version_type(version)
        with self.assertRaises(argparse.ArgumentTypeError):
            release.repository_type('owner/repo"; command')
        self.assertEqual(release.version_type('1.2.3'), '1.2.3')


if __name__ == '__main__':
    unittest.main()
