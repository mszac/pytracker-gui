"""Round-trip YAML loading and controlled field application.

Only ruamel.yaml is allowed for editing; PyYAML safe_dump would destroy comments.
"""
import hashlib
import io
from pathlib import Path
from ruamel.yaml import YAML


def make_yaml():
    yaml = YAML(typ='rt')
    yaml.preserve_quotes = True
    yaml.width = 10000
    yaml.allow_duplicate_keys = False
    return yaml


def load_text(text: str):
    doc = make_yaml().load(text)
    if not isinstance(doc, dict):
        raise ValueError('YAML musi zawierać mapę klucz: wartość na poziomie głównym.')
    return doc


def dump_doc(doc) -> str:
    out = io.StringIO()
    make_yaml().dump(doc, out)
    return out.getvalue()


def get_value(doc, dotted: str):
    value = doc
    for item in dotted.split('.'):
        if not isinstance(value, dict) or item not in value:
            return None
        value = value[item]
    return value


def update_value(doc, dotted: str, value):
    keys = dotted.split('.')
    cur = doc
    for key in keys[:-1]:
        if key not in cur or not isinstance(cur[key], dict):
            raise KeyError(f'Brak sekcji YAML: {key} w {dotted}')
        cur = cur[key]
    if keys[-1] not in cur:
        raise KeyError(f'Nieznane pole YAML: {dotted}')
    old = cur[keys[-1]]
    # Preserve scalar quoting/comments as much as ruamel permits.
    if isinstance(old, str) and isinstance(value, str) and type(old) is not str:
        cur[keys[-1]] = type(old)(value)
    else:
        cur[keys[-1]] = value


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_source(path: Path):
    contents = path.read_bytes()
    return load_text(contents.decode('utf-8-sig')), sha256(contents)
