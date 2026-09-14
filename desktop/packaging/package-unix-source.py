#!/usr/bin/env python3
"""Create the small source archive needed to compile the IRIX/Unix edition."""
import argparse
import hashlib
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def package(output, test_kit=False):
    version = (ROOT / 'desktop/packaging/version.txt').read_text().strip()
    output.mkdir(parents=True, exist_ok=True)
    name = (f'pc110-atlas-{version}-irix-test-kit' if test_kit
            else f'pc110-atlas-{version}-unix-source')
    target = output / f'{name}.tar.gz'
    prefix = name if test_kit else f'pc110-atlas-unix-{version}'
    files = [ROOT / 'unix' / name for name in (
        'Makefile', 'irix.mk', 'atlas_x11.c', 'pixel.h', 'README.md', 'tests/test_portable.c')]
    files += [ROOT / 'LICENSE', ROOT / 'LICENSING.md',
              ROOT / 'PC110Atlas/Vendor/PC110Core/pc110_core.c',
              ROOT / 'PC110Atlas/Vendor/PC110Core/include/PC110Core/PC110Core.h',
              ROOT / 'PC110Atlas/Vendor/PC110Core/README.md']
    entries = [(path, path.relative_to(ROOT).as_posix()) for path in files]
    if test_kit:
        entries += [(ROOT / 'unix/test-kit' / name, name)
                    for name in ('START-HERE.txt', 'TEST-REPORT.txt')]
    with tarfile.open(target, 'w:gz', format=tarfile.USTAR_FORMAT) as archive:
        for path, relative in entries:
            info = archive.gettarinfo(path, arcname=f'{prefix}/{relative}')
            # Avoid carrying local account names or permissions into a shared kit.
            info.uid = info.gid = 0
            info.uname = info.gname = ''
            info.mode = 0o644
            with path.open('rb') as source:
                archive.addfile(info, source)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    target.with_name(target.name + '.sha256').write_text(
        f'{digest}  {target.name}\n', encoding='ascii')
    print(target)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--test-kit', action='store_true',
                        help='Include plain-text IRIX instructions and a test report template')
    args = parser.parse_args()
    package(args.output, args.test_kit)
