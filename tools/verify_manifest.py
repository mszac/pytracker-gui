"""Verify delivered tree against release SHA-256 manifest; excludes MANIFEST itself."""
import hashlib
import sys
from pathlib import Path


def verify(root: Path):
    manifest = root / 'MANIFEST.sha256'
    expected={}
    for line in manifest.read_text(encoding='utf-8').splitlines():
        digest, rel = line.split('  ',1)
        if rel in expected:raise ValueError('Manifest duplicate: '+rel)
        if rel.startswith('/') or '..' in Path(rel).parts or rel=='MANIFEST.sha256':
            raise ValueError('Invalid manifest filename: '+rel)
        expected[rel]=digest
    actual={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and p.name != 'MANIFEST.sha256'}
    if actual!=expected:
        missing=set(expected)-set(actual);extra=set(actual)-set(expected)
        bad=[x for x in set(expected)&set(actual) if expected[x]!=actual[x]]
        raise ValueError(f'MANIFEST FAIL: missing={missing}, extra={extra}, checksum={bad}')
    print(f'MANIFEST PASS: {len(expected)}/{len(expected)} payload files')


if __name__=='__main__':
    verify(Path(__file__).resolve().parents[1])
