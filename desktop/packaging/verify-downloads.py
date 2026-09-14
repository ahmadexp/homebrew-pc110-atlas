#!/usr/bin/env python3
"""Verify the downloaded subset of a release, requiring a checksum for every file."""
import hashlib
import re
import sys
from pathlib import Path


def verify(directory):
    checksums = {}
    for line in (directory / 'SHA256SUMS').read_text().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  ([^/\\]+)', line)
        if not match or match[2] in checksums:
            raise ValueError('Malformed or duplicate SHA256SUMS entry')
        checksums[match[2]] = match[1]
    files = [p for p in directory.iterdir() if p.is_file() and p.name != 'SHA256SUMS']
    if not files:
        raise ValueError('No downloaded release assets')
    for path in files:
        checksum = hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                checksum.update(block)
        if checksum.hexdigest() != checksums.get(path.name):
            raise ValueError(f'Missing or incorrect checksum: {path.name}')
        print(f'Verified {path.name}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: verify-downloads.py DIRECTORY')
    verify(Path(sys.argv[1]))
