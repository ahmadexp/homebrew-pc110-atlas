#!/usr/bin/env python3
"""Build a small, deterministic Pi-Apps import ZIP from an explicit public allowlist."""
import argparse
import hashlib
import re
import stat
import struct
import zipfile
from pathlib import Path

APP = Path(__file__).resolve().parent / 'pi-apps' / 'PC110 Atlas'
FILES = ('credits', 'description', 'icon-24.png', 'icon-64.png',
         'install-64', 'uninstall', 'website')


def package(deb, output, app=APP):
    for name in FILES:
        path = app / name
        if path.is_symlink() or not path.is_file() or not path.stat().st_size:
            raise ValueError(f'Missing, empty, or symlinked public file: {path}')
    script = (app / 'install-64').read_text()
    version = re.search(r'^version=([0-9]+\.[0-9]+\.[0-9]+)$', script, re.M)
    checksum = re.search(r'^sha256=([0-9a-f]{64})$', script, re.M)
    if not version or not checksum:
        raise ValueError('Installer must pin a release version and SHA-256')
    if deb.name != f'pc110-atlas-{version[1]}-linux-arm64.deb' or not deb.is_file():
        raise ValueError('Provide the matching public ARM64 DEB')
    digest = hashlib.sha256()
    with deb.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    if digest.hexdigest() != checksum[1]:
        raise ValueError('DEB does not match the checksum pinned in install-64')
    for size in (24, 64):
        data = (app / f'icon-{size}.png').read_bytes()
        if (data[:8] != b'\x89PNG\r\n\x1a\n' or data[12:16] != b'IHDR'
                or len(data) < 24 or struct.unpack('>II', data[16:24]) != (size, size)):
            raise ValueError(f'icon-{size}.png must be a {size}x{size} PNG')
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation: never replace a ZIP someone may already be testing.
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for name in FILES:
            info = zipfile.ZipInfo(f'PC110 Atlas/{name}', (2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            mode = 0o775 if name in ('install-64', 'uninstall') else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (app / name).read_bytes())
    print(f'Created {output}: {len(FILES)} public files; no DEB, ROMs, or private media')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--deb', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        package(args.deb, args.output)
    except (OSError, ValueError) as error:
        parser.error(str(error))
