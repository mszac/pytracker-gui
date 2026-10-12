"""Read-only, on-demand index of GUI-owned project/run metadata.

No measurement output roots, PsychoPy, network, watcher or background thread.
A project is eligible exactly when it has a real ``experiments`` directory;
run details are opened only after explicit user selection.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from ruamel.yaml.error import YAMLError

from .catalog import BY_KEY

from .fields import APPEARANCE_FIELDS, DATASET_FIELDS, MONITOR_FIELDS, to_text
from .projects import EXPERIMENTS_DIR, PROJECT_NAME
from .yamlconfig import get_value, load_text

RUN_NAME = re.compile(r'^(\d{8}_\d{6})_([A-Za-z0-9]{5})$')
JSON_LIMIT = 512 * 1024
YAML_LIMIT = 256 * 1024


@dataclass(frozen=True)
class ProjectHistory:
    name: str
    directory: Path
    run_count: int


@dataclass(frozen=True)
class RunHistory:
    name: str
    directory: Path
    run_id: str
    timestamp: str
    journal: str


def _real_directory(path):
    return not path.is_symlink() and path.is_dir()


def _read_json(path):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > JSON_LIMIT:
        raise ValueError('Missing, linked or oversized metadata: ' + path.name)
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError('Expected a JSON object: ' + path.name)
    return value


def list_runs(project_dir):
    """List valid direct run directories, newest first, without reading their data."""
    parent = Path(project_dir) / EXPERIMENTS_DIR
    if not _real_directory(parent):
        return []
    runs = []
    for folder in parent.iterdir():
        m = RUN_NAME.fullmatch(folder.name)
        if m is None or not _real_directory(folder):
            continue
        # A journal is owned by this run only if its full name agrees with
        # the directory timestamp and case-sensitive 5-character run ID.
        logname = f'experiment_{m.group(1)}_{m.group(2)}.log'
        partial = folder / (logname + '.part')
        complete = folder / logname
        journal = ('partial' if partial.is_file() and not partial.is_symlink() else
                   'complete' if complete.is_file() and not complete.is_symlink() else 'none')
        runs.append(RunHistory(folder.name, folder, m.group(2), m.group(1), journal))
    return sorted(runs, key=lambda r: r.name, reverse=True)


def list_projects(projects_root):
    """One shallow scan of project folders; no run YAML/log/measurement data."""
    root = Path(projects_root)
    if not _real_directory(root):
        return []
    entries = []
    for folder in root.iterdir():
        if not PROJECT_NAME.fullmatch(folder.name) or not _real_directory(folder):
            continue
        if not _real_directory(folder / EXPERIMENTS_DIR):
            continue
        count = sum(1 for run in (folder / EXPERIMENTS_DIR).iterdir()
                    if RUN_NAME.fullmatch(run.name) and _real_directory(run))
        entries.append(ProjectHistory(folder.name, folder, count))
    return sorted(entries, key=lambda p: p.name.casefold())


def _scalar(value):
    if isinstance(value, (list, tuple)):
        return ', '.join(str(x) for x in value[:6])
    if isinstance(value, dict):
        return '…'
    return to_text(value)


def _yaml_fields(run_dir, plan):
    """Read one immutable snapshot only, extracting known fields, never full output CSV."""
    steps = plan.get('steps', [])
    if not isinstance(steps, list) or not steps:
        return {}, [], 'No configuration blocks in run.json'
    details = []
    first = {}
    errors = []
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append('Invalid block metadata')
            continue
        key = step.get('key')
        if not isinstance(key, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,40}', key):
            errors.append('Unsafe block key')
            continue
        path = run_dir / (key + '.yaml')
        try:
            if path.is_symlink() or not path.is_file() or path.stat().st_size > YAML_LIMIT:
                raise ValueError('Missing, linked or oversized snapshot')
            doc = load_text(path.read_text(encoding='utf-8-sig'))
            fields = {}
            for group_name, group in (('Dataset', DATASET_FIELDS), ('Monitor', MONITOR_FIELDS),
                                      ('Appearance', APPEARANCE_FIELDS)):
                present = [(field.path, _scalar(get_value(doc, field.path))) for field in group
                           if get_value(doc, field.path) is not None]
                fields[group_name] = present
            details.append((key + '.yaml', fields))
            if not first:
                first = fields
        except (OSError, ValueError, UnicodeError, YAMLError) as exc:
            errors.append(key + '.yaml: ' + str(exc))
    return first, details, '; '.join(errors)


def read_run(run, project):
    """Return a concise safe report from GUI-owned snapshots; never open experiment outputs."""
    run_dir = run.directory
    if not _real_directory(run_dir) or run_dir.parent != project.directory / EXPERIMENTS_DIR:
        raise ValueError('Run outside selected project')
    plan = _read_json(run_dir / 'run.json')
    if plan.get('run_id') != run.run_id or plan.get('started_at') != run.timestamp:
        raise ValueError('Run manifest does not match the selected run ID')
    if plan.get('project_name', project.name) != project.name:
        raise ValueError('Manifest project name mismatch')
    try:
        settings = _read_json(run_dir / 'gui-settings.json')
    except (OSError, ValueError, UnicodeError):
        settings = {}
    try:
        result = _read_json(run_dir / 'result.json')
        process_status = str(result.get('status', 'Unknown'))[:200]
    except (OSError, ValueError, UnicodeError):
        process_status = 'Not recorded'
    first, details, errors = _yaml_fields(run_dir, plan)
    steps = plan.get('steps', [])
    if not isinstance(steps, list):
        steps = []
    trials = ', '.join(f'{s.get("key", "?")}: {s.get("trials", "?")}' for s in steps if isinstance(s, dict))
    fields = {group: dict(items) for group, items in first.items()}
    dataset = fields.get('Dataset', {})
    monitor = fields.get('Monitor', {})
    appearance = fields.get('Appearance', {})
    data_keys = [k for k in dataset if k.startswith('dataset.') and k.endswith('.path')]
    data_path = dataset.get(data_keys[0], '—') if data_keys else '—'
    return {
        'project': project.name, 'run_id': run.run_id, 'started': run.timestamp,
        'demo_key': str(plan.get('demo_key', '—')),
        'variant': ((BY_KEY[plan['demo_key']].label + ' · ' + BY_KEY[plan['demo_key']].variant)
                    if plan.get('demo_key') in BY_KEY else str(plan.get('demo_key', '—'))),
        'journal': run.journal,
        'process_status': process_status, 'gaze': str(plan.get('gaze', '—')),
        'python': Path(str(plan.get('python', '—'))).name,
        'eye': Path(str(plan.get('eye_config', '—'))).name,
        'voice': bool(plan.get('voice', False)), 'raw_data': bool(plan.get('raw_data', False)),
        'log_level': str(plan.get('log_level', '—')), 'trials': trials or '—',
        'blocks': len(steps), 'data': Path(data_path).name if data_path != '—' else '—',
        'data_path': data_path,
        'monitor': monitor.get('display.monitor.name', '—'),
        'resolution': monitor.get('display.monitor.resolution', '—'),
        'button_size': appearance.get('display.gui.button.size', '—'),
        'font_size': appearance.get('display.gui.button.text.size', '—'),
        'snapshots': ', '.join(str(s.get('key', '')) + '.yaml' for s in steps if isinstance(s, dict)),
        'gui_state': settings.get('gui', {}) if isinstance(settings.get('gui', {}), dict) else {},
        'yaml_details': details, 'yaml_errors': errors,
    }
