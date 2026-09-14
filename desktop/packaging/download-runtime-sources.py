#!/usr/bin/env python3
"""Include checksum-pinned runtime sources and build inputs with desktop releases."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def download(output):
    output.mkdir(parents=True, exist_ok=True)
    files = json.loads(Path(__file__).with_name('runtime-source-files.json').read_text())
    for entry in files:
        name = entry['name']
        if Path(name).name != name or not entry['url'].startswith('https://github.com/adoptium/'):
            raise ValueError('Unexpected runtime source destination')
        target = output / name
        if not target.exists():
            subprocess.run(['curl', '--fail', '--location', '--retry', '3', '--silent', '--show-error',
                            '--output', str(target), entry['url']], check=True)
        digest = hashlib.sha256()
        with target.open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(block)
        if digest.hexdigest() != entry['sha256']:
            raise ValueError(f'Runtime source checksum mismatch: {name}')
        print(f'Verified runtime source: {name}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    download(parser.parse_args().output)
