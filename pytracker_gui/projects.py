"""Portable, low-overhead project directories; no upstream/runtime dependency."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .storage import atomic_write

PROJECT_NAME = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$')
# Project-local execution metadata, separate from reusable project settings.
EXPERIMENTS_DIR = 'experiments'


class ProjectError(ValueError):
    pass


class ProjectStore:
    def __init__(self, root):
        self.root = Path(root)

    def directory(self, name):
        if not PROJECT_NAME.fullmatch(name):
            raise ProjectError('Project name must contain 1–64 letters, numbers, _ or -, and start with a letter or number.')
        return self.root / name

    def projects_for(self, demo_key):
        if not self.root.is_dir():
            return []
        found = []
        for directory in self.root.iterdir():
            if not directory.is_dir() or not PROJECT_NAME.fullmatch(directory.name):
                continue
            try:
                meta = json.loads((directory / 'project.json').read_text(encoding='utf-8'))
            except (OSError, ValueError):
                continue
            if meta.get('schema') == 1 and meta.get('demo_key') == demo_key and meta.get('name') == directory.name:
                found.append(directory.name)
        return sorted(found, key=str.casefold)

    def ensure(self, name, demo_key):
        directory = self.directory(name)
        existing = directory / 'project.json'
        if existing.is_file():
            try:
                meta = json.loads(existing.read_text(encoding='utf-8'))
            except (OSError, ValueError) as exc:
                raise ProjectError('Cannot read project metadata: ' + str(existing)) from exc
            if (meta.get('schema'), meta.get('demo_key'), meta.get('name')) != (1, demo_key, name):
                raise ProjectError('Existing project belongs to another demo or has invalid metadata')
            return directory
        if directory.exists() and any(directory.iterdir()):
            raise ProjectError('Project folder exists without project.json: ' + str(directory))
        directory.mkdir(parents=True, exist_ok=True)
        atomic_write(existing, (json.dumps({'schema': 1, 'name': name, 'demo_key': demo_key},
                                           indent=2) + '\n').encode('utf-8'), backup=False)
        return directory


def portable_eye_reference(path, upstream):
    """Use a checkout-relative reference whenever the ioHub file is inside upstream."""
    p = Path(path).expanduser().resolve()
    root = Path(upstream).expanduser().resolve()
    try:
        return {'base': 'upstream', 'path': p.relative_to(root).as_posix()}
    except ValueError:
        return {'base': 'external', 'path': str(p)}


def resolve_eye_reference(reference, upstream):
    if reference.get('base') == 'upstream':
        root = Path(upstream).expanduser().resolve()
        target = (root / reference['path']).resolve()
        if target.is_relative_to(root):
            return str(target)
    return reference.get('path', '')
