"""Read-only parameter documentation shared by the GUI and manual renderer.

The packaged JSON is independent of YAML parsers, PsychoPy, Git and network access.
"""
import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def parameter_catalog():
    path = Path(__file__).with_name('parameter_help.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    items = data['parameters']
    if data.get('schema_version') != 1:
        raise ValueError('Unsupported parameter help schema')
    if len(items) != len({item['key'] for item in items}):
        raise ValueError('Duplicate parameter help keys')
    return {item['key']: item for item in items}


@lru_cache(maxsize=1)
def english_tooltip_catalog():
    """English titles, short tooltip text, and extended manual descriptions."""
    path = Path(__file__).with_name('parameter_help_en.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('schema_version') != 1:
        raise ValueError('Unsupported English tooltip schema')
    if set(data['parameters']) != set(parameter_catalog()):
        raise ValueError('English tooltip coverage must match the Polish catalog')
    return data['parameters']


def get_parameter_help(key, language='pl'):
    """Return a localized record; stable source/status metadata comes from Polish registry."""
    record = parameter_catalog()[key]
    if language == 'pl':
        return record
    if language != 'en':
        raise ValueError('Unsupported language: ' + str(language))
    overlay = english_tooltip_catalog()[key]
    return {**record, **overlay}
