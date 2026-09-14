#!/usr/bin/env python3
"""Integration test: real DEB/RPM metadata, ephemeral signing key, and APT client."""
import importlib.util
import os
import subprocess
import tempfile
from pathlib import Path

script = Path(__file__).resolve().parents[1] / 'build-repositories.py'
spec = importlib.util.spec_from_file_location('repositories', script)
repositories = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repositories)


def run(*args, **kwargs):
    return subprocess.check_output(args, text=True, **kwargs)


with tempfile.TemporaryDirectory(prefix='pc110-repository-test-') as temporary:
    root = Path(temporary)
    assets = root / 'assets'
    assets.mkdir()
    for arch in ('amd64', 'arm64'):
        source = root / arch
        (source / 'DEBIAN').mkdir(parents=True)
        (source / 'DEBIAN/control').write_text(
            f'Package: pc110-atlas\nVersion: 1.2.3\nArchitecture: {arch}\n'
            'Maintainer: Package Test <test@example.invalid>\nDescription: Repository integration test\n')
        (source / 'usr/share/pc110-atlas').mkdir(parents=True)
        (source / 'usr/share/pc110-atlas/test.txt').write_text(arch)
        run('dpkg-deb', '--build', '--root-owner-group', str(source), str(assets / f'pc110-atlas_{arch}.deb'))
    rpm_root = root / 'rpmbuild'
    for name in ('BUILD', 'BUILDROOT', 'RPMS', 'SOURCES', 'SPECS', 'SRPMS'):
        (rpm_root / name).mkdir(parents=True)
    rpm_spec = rpm_root / 'SPECS/test.spec'
    rpm_spec.write_text('''Name: pc110-atlas
Version: 1.2.3
Release: 1
Summary: Repository integration test
License: LicenseRef-PC110-Atlas
BuildArch: x86_64
%description
Repository integration test.
%install
mkdir -p %{buildroot}/usr/share/pc110-atlas
echo test > %{buildroot}/usr/share/pc110-atlas/test.txt
%files
/usr/share/pc110-atlas/test.txt
''')
    run('rpmbuild', '--define', f'_topdir {rpm_root}', '-bb', str(rpm_spec))
    import shutil
    for package in (rpm_root / 'RPMS').rglob('*.rpm'):
        shutil.copy2(package, assets / package.name)
    gnupg = root / 'gnupg'
    gnupg.mkdir(mode=0o700)
    previous_home = os.environ.get('GNUPGHOME')
    os.environ['GNUPGHOME'] = str(gnupg)
    try:
        run('gpg', '--batch', '--passphrase', '', '--quick-generate-key',
            'PC110 Repository Test <test@example.invalid>', 'rsa2048', 'sign', '1d')
        keys = run('gpg', '--batch', '--with-colons', '--list-secret-keys')
        key = next(line.split(':')[9] for line in keys.splitlines() if line.startswith('fpr:'))
        output = root / 'repository'
        repositories.build(assets, output, 'https://example.invalid/pc110', key)
        for arch in ('amd64', 'arm64'):
            content = (output / f'apt/dists/stable/main/binary-{arch}/Packages').read_text()
            assert content.count('Package: pc110-atlas') == 1
            assert f'Architecture: {arch}\n' in content
            assert 'Filename: pool/' in content
        rpm_db = root / 'rpmdb'
        run('rpm', '--dbpath', str(rpm_db), '--initdb')
        run('rpm', '--dbpath', str(rpm_db), '--import', str(output / 'keys/pc110-atlas.asc'))
        package = next((output / 'rpm/x86_64/Packages').glob('*.rpm'))
        signature = run('rpm', '--dbpath', str(rpm_db), '--checksig', str(package))
        assert 'signatures OK' in signature, signature
        lists = root / 'lists'
        (lists / 'partial').mkdir(parents=True)
        sources = root / 'sources.list'
        sources.write_text(f'deb [signed-by={output}/keys/pc110-atlas.gpg] file:{output}/apt stable main\n')
        options = ['-o', f'Dir::Etc::sourcelist={sources}', '-o', 'Dir::Etc::sourceparts=-',
                   '-o', f'Dir::State::Lists={lists}', '-o', 'APT::Architecture=amd64',
                   '-o', 'APT::Sandbox::User=root', '-o', 'Debug::NoLocking=true']
        run('apt-get', *options, 'update')
        policy = run('apt-cache', *options, 'policy', 'pc110-atlas')
        assert '1.2.3' in policy, policy
        # A modified signed Release must fail signature verification.
        signed = output / 'apt/dists/stable/InRelease'
        signed.write_text(signed.read_text().replace('Origin: PC110 Atlas', 'Origin: Tampered'))
        assert subprocess.run(['gpg', '--verify', str(signed)], stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL).returncode != 0
        print('APT accepted signed metadata; architectures, RPM signatures, and tamper rejection passed')
    finally:
        subprocess.run(['gpgconf', '--kill', 'all'], check=False)
        if previous_home is None:
            os.environ.pop('GNUPGHOME', None)
        else:
            os.environ['GNUPGHOME'] = previous_home
