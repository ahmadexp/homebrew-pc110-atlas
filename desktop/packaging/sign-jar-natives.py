#!/usr/bin/env python3
"""Sign native libraries inside JARs before signing the enclosing macOS app."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import tempfile
import zipfile


def sign_jar(jar, signer, native_overrides=None):
    with zipfile.ZipFile(jar) as archive:
        entries = archive.infolist()
        libraries = [item for item in entries if item.filename.endswith(('.dylib', '.jnilib')) or
                     (item.filename.startswith('qemu/macos-') and
                      item.filename.endswith(('/qemu-system-i386', '.dylib.bin')))]
        if not libraries:
            return 0
        if len({item.filename for item in entries}) != len(entries):
            raise ValueError(f'Duplicate archive entries: {jar}')
        if any(item.filename.upper().startswith('META-INF/') and
               item.filename.upper().endswith(('.SF', '.RSA', '.DSA', '.EC')) for item in entries):
            raise ValueError(f'Refusing to invalidate an existing Java archive signature: {jar}')
        replacements = {}
        for item in libraries:
            original = archive.read(item)
            signed = signer((native_overrides or {}).get(item.filename, original))
            replacements[item.filename] = signed
            checksum = item.filename + '.sha256'
            if checksum in archive.namelist():
                # Skiko uses this digest to choose its extracted-library cache.
                replacements[checksum] = hashlib.sha256(signed).hexdigest().encode('ascii')
        # The QEMU host verifies every extracted runtime file. Signing changes
        # executable bytes, so seal the manifest with those same signed bytes.
        for item in entries:
            if not (item.filename.startswith('qemu/macos-') and item.filename.endswith('/files.sha256')):
                continue
            prefix = item.filename.removesuffix('files.sha256')
            lines = []
            for line in archive.read(item).decode('utf-8').splitlines():
                _, name = line.split('  ', 1)
                entry_name = prefix + name + ('.bin' if name.endswith('.dylib') else '')
                data = replacements.get(entry_name)
                if data is None:
                    data = archive.read(entry_name)
                lines.append(f'{hashlib.sha256(data).hexdigest()}  {name}\n')
            replacements[item.filename] = ''.join(lines).encode('utf-8')
        with tempfile.TemporaryDirectory(prefix='pc110-signed-jar-', dir=jar.parent) as scratch:
            output = Path(scratch) / jar.name
            with zipfile.ZipFile(output, 'w') as target:
                target.comment = archive.comment
                for item in entries:
                    data = replacements.get(item.filename)
                    target.writestr(item, archive.read(item) if data is None else data)
            output.chmod(jar.stat().st_mode & 0o777)
            output.replace(jar)
    return len(libraries)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--identity', required=True)
    parser.add_argument('--pc110-native-library', type=Path,
                        help='Optional same-architecture PC110 core rebuilt for the minimum macOS')
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error('Expected the packaged app Contents/app directory')
    if not args.identity.startswith('Developer ID Application: '):
        parser.error('A Developer ID Application identity is required')
    jars = sorted(args.directory.glob('*.jar'))
    overrides = {}
    if args.pc110_native_library:
        executable = args.directory.parent / 'MacOS' / 'PC110 Atlas'
        expected = subprocess.check_output(['lipo', '-archs', str(executable)]).strip()
        actual = subprocess.check_output(['lipo', '-archs', str(args.pc110_native_library)]).strip()
        if actual != expected:
            parser.error('Replacement native library architecture does not match the app launcher')
        core_entry = 'native/libpc110_desktop.dylib'
        count = 0
        for jar in jars:
            with zipfile.ZipFile(jar) as archive:
                count += archive.namelist().count(core_entry)
        if count != 1:
            parser.error('Expected exactly one packaged PC110 native library')
        overrides[core_entry] = args.pc110_native_library.read_bytes()

    def signer(data):
        with tempfile.TemporaryDirectory(prefix='pc110-native-sign-') as scratch:
            library = Path(scratch) / 'library.dylib'
            library.write_bytes(data)
            subprocess.run(['codesign', '--force', '--timestamp', '--options', 'runtime',
                            '--sign', args.identity, str(library)], check=True)
            subprocess.run(['codesign', '--verify', '--strict', str(library)], check=True)
            return library.read_bytes()

    total = 0
    for jar in jars:
        count = sign_jar(jar, signer, overrides)
        if count:
            print(f'Signed {count} native libraries in {jar.name}')
            total += count
    print(f'Signed {total} archived native libraries, including all bundled architectures.')


if __name__ == '__main__':
    main()
