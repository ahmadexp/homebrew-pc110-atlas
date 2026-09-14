#!/usr/bin/env python3
"""Build signed APT and YUM/DNF repositories in a new static hosting directory."""
import argparse
import gzip
import html
import os
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse


def run(*args, cwd=None, output=None):
    result = subprocess.run(args, cwd=cwd, check=True, stdout=subprocess.PIPE if output else None)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(result.stdout)


def sign(path, key, clear=False):
    target = path.with_name('InRelease') if clear else Path(str(path) + ('.gpg' if path.name == 'Release' else '.asc'))
    run('gpg', '--batch', '--yes', '--local-user', key, '--armor', '--output', str(target),
        '--clearsign' if clear else '--detach-sign', str(path))
    if clear:
        run('gpg', '--verify', str(target))
    else:
        run('gpg', '--verify', str(target), str(path))


def build(assets, output, base_url, key):
    assets, output = assets.resolve(), output.resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError('Output must be empty; publish the new repository atomically')
    if not re.fullmatch(r'[A-Fa-f0-9]{40}|[A-Fa-f0-9]{64}', key):
        raise ValueError('Use the full GPG signing-key fingerprint')
    parsed = urlparse(base_url)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError('Repository base URL must be HTTPS without query or fragment')
    if any(c.isspace() for c in base_url):
        raise ValueError('Repository base URL must not contain whitespace')
    base_url = base_url.rstrip('/')
    for command in ('apt-ftparchive', 'dpkg-deb', 'rpm', 'rpmsign', 'createrepo_c', 'gpg'):
        if not shutil.which(command):
            raise ValueError(f'Missing required tool: {command}')
    debs, rpms = sorted(assets.glob('*.deb')), sorted(assets.glob('*.rpm'))
    if not debs or not rpms:
        raise ValueError('Both DEB and RPM release artifacts are required')
    for deb in debs:
        if subprocess.check_output(['dpkg-deb', '-f', str(deb), 'Package'], text=True).strip() != 'pc110-atlas':
            raise ValueError(f'Unexpected Debian package name: {deb}')
    for rpm in rpms:
        if subprocess.check_output(['rpm', '-qp', '--qf', '%{NAME}', str(rpm)], text=True).strip() != 'pc110-atlas':
            raise ValueError(f'Unexpected RPM package name: {rpm}')

    output.mkdir(parents=True, exist_ok=True)
    run('gpg', '--batch', '--armor', '--export', key, output=output / 'keys/pc110-atlas.asc')
    run('gpg', '--batch', '--export', key, output=output / 'keys/pc110-atlas.gpg')
    if not (output / 'keys/pc110-atlas.gpg').stat().st_size:
        raise ValueError('GPG public key was not exported')

    apt = output / 'apt'
    pool = apt / 'pool/main/p/pc110-atlas'
    pool.mkdir(parents=True)
    architectures = set()
    for deb in debs:
        arch = subprocess.check_output(['dpkg-deb', '-f', str(deb), 'Architecture'], text=True).strip()
        if arch not in ('amd64', 'arm64'):
            raise ValueError(f'Unsupported DEB architecture: {arch}')
        architectures.add(arch)
        shutil.copy2(deb, pool / deb.name)
    for arch in sorted(architectures):
        packages = apt / f'dists/stable/main/binary-{arch}/Packages'
        run('apt-ftparchive', '-a', arch, 'packages', 'pool', cwd=apt, output=packages)
        packages.with_suffix('.gz').write_bytes(gzip.compress(packages.read_bytes(), mtime=0))
    release = apt / 'dists/stable/Release'
    run('apt-ftparchive', '-o', 'APT::FTPArchive::Release::Origin=PC110 Atlas',
        '-o', 'APT::FTPArchive::Release::Label=PC110 Atlas',
        '-o', 'APT::FTPArchive::Release::Suite=stable',
        '-o', 'APT::FTPArchive::Release::Codename=stable',
        '-o', f'APT::FTPArchive::Release::Architectures={" ".join(sorted(architectures))}',
        '-o', 'APT::FTPArchive::Release::Components=main',
        'release', 'dists/stable', cwd=apt, output=release)
    sign(release, key, clear=True)
    sign(release, key)

    rpm_architectures = set()
    for rpm in rpms:
        arch = subprocess.check_output(['rpm', '-qp', '--qf', '%{ARCH}', str(rpm)], text=True).strip()
        if arch not in ('x86_64', 'aarch64'):
            raise ValueError(f'Unsupported RPM architecture: {arch}')
        rpm_architectures.add(arch)
        target = output / f'rpm/{arch}/Packages/{rpm.name}'
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(rpm, target)
        run('rpmsign', '--define', f'_gpg_name {key}', '--define', f'__gpg {shutil.which("gpg")}',
            '--define', '_gpg_digest_algo sha256', '--addsign', str(target))
    for arch in sorted(rpm_architectures):
        repository = output / 'rpm' / arch
        run('createrepo_c', str(repository))
        sign(repository / 'repodata/repomd.xml', key)
    (output / 'pc110-atlas.repo').write_text(
        '[pc110-atlas]\nname=PC110 Atlas\n'
        f'baseurl={base_url}/rpm/$basearch\nenabled=1\n'
        'gpgcheck=1\nrepo_gpgcheck=1\n'
        f'gpgkey={base_url}/keys/pc110-atlas.asc\n'
    )
    (output / '.nojekyll').touch()
    (output / 'keys/fingerprint.txt').write_text(key.upper() + '\n')
    apt_commands = f'''curl -fsSLo pc110-atlas.asc {base_url}/keys/pc110-atlas.asc
gpg --show-keys --fingerprint pc110-atlas.asc
# Compare with the fingerprint above before continuing.
gpg --dearmor --output pc110-atlas.gpg pc110-atlas.asc
sudo install -m 644 pc110-atlas.gpg /usr/share/keyrings/pc110-atlas.gpg
echo 'deb [signed-by=/usr/share/keyrings/pc110-atlas.gpg] {base_url}/apt stable main' | sudo tee /etc/apt/sources.list.d/pc110-atlas.list
sudo apt update
sudo apt install pc110-atlas'''
    rpm_commands = f'''curl -fsSLo pc110-atlas.repo {base_url}/pc110-atlas.repo
sudo install -m 644 pc110-atlas.repo /etc/yum.repos.d/pc110-atlas.repo
sudo dnf install pc110-atlas
# Or: sudo yum install pc110-atlas'''
    (output / 'index.html').write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>PC110 Atlas packages</title>'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<style>body{max-width:64rem;margin:3rem auto;padding:0 1rem;font:17px/1.6 system-ui}'
        'pre{overflow:auto;padding:1rem;background:#f2f4f6}code{font-size:.9em}</style>'
        '<h1>PC110 Atlas packages</h1><p>Signed APT and YUM/DNF repositories.</p>'
        '<p>Portable desktop edition. Bring your own compatible BIOS and disk images.</p>'
        f'<h2>Signing-key fingerprint</h2><pre>{html.escape(key.upper())}</pre>'
        '<p>Verify this fingerprint against the public distribution repository before trusting the key.</p>'
        '<p><a href="keys/pc110-atlas.asc">Signing key</a> | '
        '<a href="pc110-atlas.repo">YUM/DNF configuration</a> | '
        '<a href="https://github.com/ahmadexp/homebrew-pc110-atlas">Releases and support</a></p>'
        f'<h2>Ubuntu / Debian</h2><pre><code>{html.escape(apt_commands)}</code></pre>'
        '<p>Built on Ubuntu 24.04. Install on distributions that satisfy the package dependencies.</p>'
        f'<h2>YUM / DNF</h2><pre><code>{html.escape(rpm_commands)}</code></pre>'
        '<p>Check the key fingerprint when prompted. Package and repository signature checks are enabled.</p>'
        '</html>\n'
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--key', default=os.environ.get('LINUX_GPG_KEY_ID'), required=not os.environ.get('LINUX_GPG_KEY_ID'))
    try:
        build(**vars(parser.parse_args()))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
