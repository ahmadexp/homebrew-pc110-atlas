#!/usr/bin/env python3
"""Normalize installers and render package manifests from their actual bytes."""
import argparse
import hashlib
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGING = ROOT / "desktop/packaging"


def version_type(value):
    if not re.fullmatch(r"[1-9][0-9]*\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", value):
        raise argparse.ArgumentTypeError("Use a stable MAJOR.MINOR.PATCH desktop version")
    if any(n > limit for n, limit in zip(map(int, value.split('.')), (255, 255, 65535))):
        raise argparse.ArgumentTypeError("Version exceeds Windows MSI limits")
    return value


def repository_type(value):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value):
        raise argparse.ArgumentTypeError("Repository must be GitHub OWNER/REPO")
    return value


def digest(path):
    checksum = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            checksum.update(block)
    return checksum.hexdigest()


def render(source, destination, values):
    content = source.read_text()
    for key, value in values.items():
        content = content.replace(f"@{key}@", value)
    if re.search(r"@[A-Z0-9_]+@", content):
        raise ValueError(f"Unresolved template token in {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content)


def collect(source, output, version, platform, arch):
    formats = {'linux': ('deb', 'rpm'), 'windows': ('msi', 'exe'), 'macos': ('dmg',)}[platform]
    output.mkdir(parents=True, exist_ok=True)
    for extension in formats:
        candidates = sorted(source.glob(f'{extension}/*.{extension}'))
        if len(candidates) != 1:
            raise ValueError(f"Expected one {extension} in {source}, found {len(candidates)}. Clean old packages first.")
        target = output / f'pc110-atlas-{version}-{platform}-{arch}.{extension}'
        if target.exists():
            raise ValueError(f"Refusing to overwrite {target}")
        shutil.copy2(candidates[0], target)


def manifests(assets, output, version, repository, channel='all'):
    values = {'VERSION': version, 'REPOSITORY': repository}
    for key, platform, arch, extension in [
        ('WINDOWS_SHA256', 'windows', 'x64', 'msi'),
        ('MAC_ARM64_SHA256', 'macos', 'arm64', 'dmg'),
        ('MAC_X64_SHA256', 'macos', 'x64', 'dmg'),
    ]:
        if channel == 'chocolatey' and platform != 'windows':
            continue
        if channel == 'homebrew' and platform != 'macos':
            continue
        artifact = assets / f'pc110-atlas-{version}-{platform}-{arch}.{extension}'
        if not artifact.is_file() or artifact.stat().st_size == 0:
            raise ValueError(f"Missing or empty release artifact: {artifact}")
        values[key] = digest(artifact)
    if channel in ('all', 'homebrew'):
        render(PACKAGING / 'homebrew/pc110-atlas.rb.in', output / 'homebrew/Casks/pc110-atlas.rb', values)
    if channel in ('all', 'chocolatey'):
        render(PACKAGING / 'chocolatey/pc110-atlas.nuspec.in', output / 'chocolatey/pc110-atlas.nuspec', values)
        render(PACKAGING / 'chocolatey/chocolateyInstall.ps1.in', output / 'chocolatey/tools/chocolateyInstall.ps1', values)


def checksums(assets, update_file=None):
    if update_file is not None:
        if (not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', update_file)
                or update_file in ('SHA256SUMS', 'SHA256SUMS.asc')):
            raise ValueError('Checksum update requires a release artifact filename')
        manifest = assets / 'SHA256SUMS'
        entries = {}
        for line in manifest.read_text().splitlines():
            match = re.fullmatch(r'([0-9a-f]{64})  ([^/\\]+)', line)
            if not match or match[2] in entries:
                raise ValueError('Malformed or duplicate SHA256SUMS entry')
            entries[match[2]] = match[1]
        artifact = assets / update_file
        if not artifact.is_file() or artifact.stat().st_size == 0:
            raise ValueError(f'Missing or empty release artifact: {artifact}')
        entries[update_file] = digest(artifact)
        manifest.write_text(''.join(f'{checksum}  {name}\n' for name, checksum in entries.items()),
                            encoding='utf-8', newline='\n')
        return
    files = sorted(p for p in assets.iterdir() if p.is_file() and p.name not in ('SHA256SUMS', 'SHA256SUMS.asc'))
    if not files:
        raise ValueError('No release artifacts to checksum')
    (assets / 'SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.name}\n' for p in files),
                                     encoding='utf-8', newline='\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    collect_parser = sub.add_parser('collect')
    collect_parser.add_argument('--source', type=Path, default=ROOT / 'desktop/build/compose/binaries/main')
    collect_parser.add_argument('--output', type=Path, required=True)
    collect_parser.add_argument('--version', type=version_type, required=True)
    collect_parser.add_argument('--platform', choices=('linux', 'windows', 'macos'), required=True)
    collect_parser.add_argument('--arch', choices=('x64', 'arm64'), required=True)
    render_parser = sub.add_parser('manifests')
    render_parser.add_argument('--assets', type=Path, required=True)
    render_parser.add_argument('--output', type=Path, required=True)
    render_parser.add_argument('--version', type=version_type, required=True)
    render_parser.add_argument('--repository', type=repository_type, default='ahmadexp/homebrew-pc110-atlas')
    render_parser.add_argument('--channel', choices=('all', 'homebrew', 'chocolatey'), default='all')
    checksum_parser = sub.add_parser('checksums')
    checksum_parser.add_argument('--assets', type=Path, required=True)
    checksum_parser.add_argument('--update-file', help='Update only this artifact, preserving other release checksums')
    args = vars(parser.parse_args())
    command = args.pop('command')
    try:
        {'collect': collect, 'manifests': manifests, 'checksums': checksums}[command](**args)
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
