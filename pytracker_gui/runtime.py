"""Native demo launch contracts and immutable per-run YAML snapshots.

No imports of PsychoPy, ioHub, or demo runtime code in the GUI process.
"""
from __future__ import annotations

import json
import hashlib
import os
import sys
import time
import secrets
import string
from pathlib import Path

from .catalog import BY_KEY
from .storage import atomic_write
from .validation import validate_config, resolve_path
from .layout import validate_layout
from .projects import EXPERIMENTS_DIR, portable_eye_reference
from .yamlconfig import dump_doc, get_value, read_source, update_value

# IDs refer only to the seven explicitly audited existing demonstration variants.
RUNNERS = {
    'test_en': ('test_demo', None),
    'ux_en': ('ux_ab_demo', 'text'),
    'ux_pl': ('ux_ab_demo', 'text'),
    'ts_machine_pv': ('timeseries_noise_demo', None),
    'search_en': ('text_search_demo', 'text'),
    'search_pl': ('text_search_demo', 'text'),
    'image_en': ('image_semantic_demo', 'image'),
}


class LaunchError(ValueError):
    """Safe preflight failed before creating a child process."""


def find_exact_session(step):
    """Find a session only inside the unique output root reserved for this GUI run.

    Unlike a timestamp/mtime lookup under the shared output directory, this
    resolver fails closed if zero or multiple CSV sessions are found. It never
    searches an unrelated experiment's output root.
    """
    root = Path(step['output_folder']).resolve()
    if not root.is_dir():
        return None, 'output directory missing'
    sessions = []
    for candidate in root.iterdir():
        if candidate.is_symlink() or not candidate.is_dir():
            continue
        csv_file = candidate / 'data.csv'
        if csv_file.is_symlink():
            continue
        if csv_file.is_file():
            sessions.append(candidate.resolve())
    if len(sessions) != 1:
        return None, f'expected exactly one session with data.csv; found {len(sessions)}'
    return sessions[0], None


def session_binding(step):
    """Small provenance record generated only after a child has finished."""
    session, reason = find_exact_session(step)
    record = {'block':step['key'], 'output_root':step['output_folder'],
              'configured_output_root':step['configured_output_folder'],
              'state':'linked' if session is not None else 'unresolved'}
    if session is None:
        record['reason'] = reason
    else:
        csv_file = session / 'data.csv'
        record['session_dir'] = str(session)
        record['data_csv'] = str(csv_file)
        record['data_csv_bytes'] = csv_file.stat().st_size
    return record


def preflight(demo_key, docs, loops, *, demo_root, upstream, python, gaze, eye, voice, raw_data, log_level):
    errors = list(validate_layout(upstream, demo_root))
    demo = BY_KEY.get(demo_key)
    if demo is None or demo_key not in RUNNERS:
        errors.append('Unknown demonstration ID')
        return errors
    if RUNNERS[demo_key][1] is not None:
        adapter_file = Path(demo_root) / 'tools' / 'demo_runtime_adapters.py'
        if not adapter_file.is_file():
            errors.append('Missing demo runtime adapter: ' + str(adapter_file) +
                          ' (check the original tobii-pytracker-demo checkout)')
    if not Path(python).is_file():
        errors.append('Python interpreter file does not exist: ' + str(python))
    if gaze not in ('none', 'mouse', 'tobii'):
        errors.append('Invalid gaze mode')
    if not Path(eye).is_file() or not Path(eye).suffix.lower() in ('.yaml', '.yml'):
        errors.append('An existing ioHub YAML file is required (even for NO_GAZE)')
    if raw_data and gaze == 'none':
        errors.append('Raw gaze data cannot be recorded with NO_GAZE')
    if log_level not in ('debug', 'info', 'warning', 'error', 'critical'):
        errors.append('Unsupported log level')
    for block in demo.blocks:
        if block.key not in docs:
            errors.append('Missing YAML for block ' + block.key)
            continue
        for finding in validate_config(docs[block.key], Path(demo_root), demo.modality):
            if finding.level == 'BLOCK':
                errors.append(block.name + ': ' + finding.detail)
        try:
            n = int(loops[block.key])
            if str(loops[block.key]).strip() != str(n) or not 1 <= n <= block.trials:
                raise ValueError()
        except (ValueError, TypeError, KeyError):
            errors.append(block.name + ': trial count must be 1–' + str(block.trials))
    return errors


def prepare_run(*, home, demo_key, docs, loops, demo_root, upstream, python, gaze, eye,
                voice=False, raw_data=False, log_level='info', project_dir=None, gui_settings=None):
    """Generate an immutable, per-run manifest and exact YAML bytes outside source trees."""
    up = Path(upstream).expanduser().resolve()
    root = Path(demo_root).expanduser().resolve()
    exe = Path(python).expanduser().resolve()
    eye_file = Path(eye).expanduser().resolve()
    issues = preflight(demo_key, docs, loops, demo_root= root, upstream=up, python=exe,
                       gaze=gaze, eye=eye_file, voice=voice, raw_data=raw_data, log_level=log_level)
    if issues:
        raise LaunchError('\n'.join(issues))
    demo = BY_KEY[demo_key]
    # Execution artifacts live only under <project>/experiments/<time>_<id>.
    # Standalone callers use a test/private home, never the old runs/ layout.
    base = (Path(project_dir).expanduser().resolve() if project_dir is not None else
            Path(home).expanduser().resolve())
    parent = base / EXPERIMENTS_DIR
    if project_dir is None and (parent.is_relative_to(up) or parent.is_relative_to(root)):
        raise LaunchError('Experiment snapshots must be stored outside the source repositories')
    parent.mkdir(parents=True, exist_ok=True)
    alphabet = string.ascii_letters + string.digits
    for _ in range(64):
        timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        run_id = ''.join(secrets.choice(alphabet) for _ in range(5))
        run_dir = parent / (timestamp + '_' + run_id)
        try:
            run_dir.mkdir(exist_ok=False)
            break
        except FileExistsError:
            continue
    else:
        raise LaunchError('Could not allocate a unique 5-character experiment ID')
    steps = []
    for block in demo.blocks:
        snapshot = run_dir / (block.key+'.yaml')
        out = str(get_value(docs[block.key], 'output.folder'))
        mode = demo.modality
        dataset_path=str(get_value(docs[block.key], 'dataset.'+mode+'.path'))
        source_doc,source_hash=read_source(root/block.config_relpath)
        original_path=str(get_value(source_doc,'dataset.'+mode+'.path'))
        eligibility=(int(loops[block.key])==block.trials and gaze!='none' and
                     resolve_path(root,dataset_path)==resolve_path(root,original_path))
        if demo_key=='ts_machine_pv' and Path(out).name != block.key:
            eligibility=False
        # Preserve the user's original output parent. Reserve a *new, empty*
        # child directory containing this run's case-sensitive ID. Upstream
        # creates exactly one timestamped measurement session below it.
        original_output = resolve_path(root, out)
        unique_output = original_output / ('pytracker_' + run_dir.name + '_' + block.key)
        try:
            unique_output.mkdir(parents=True, exist_ok=False)
        except FileExistsError as exc:
            raise LaunchError('Measurement output directory already exists: ' + str(unique_output)) from exc
        # Only mutate the per-run YAML copy; editor and reusable profile remain unchanged.
        from .yamlconfig import load_text
        run_doc = load_text(dump_doc(docs[block.key]))
        update_value(run_doc, 'output.folder', str(unique_output))
        atomic_write(snapshot, dump_doc(run_doc).encode('utf-8'), backup=False)
        steps.append({'key':block.key,'name':block.name,'config':str(snapshot),
                      'config_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),
                      'source_config_sha256':source_hash,
                      'trials':int(loops[block.key]),'full_trials':block.trials,
                      'dataset_path':str(resolve_path(root,dataset_path)),
                      'validator_eligible':eligibility,
                      'configured_output_folder':str(original_output),
                      'output_folder':str(unique_output)})
    # Copy the exact ioHub file for future reference without changing the runtime
    # argument, so relative includes/loader behavior remain unchanged.
    if project_dir is not None:
        atomic_write(run_dir / 'eyetracker.yaml', eye_file.read_bytes(), backup=False)
        state = {'schema': 1, 'demo_key': demo_key,
                 'run_id': run_id, 'started_at': timestamp,
                 'environment': {'upstream': '.', 'demo_root': 'tobii-pytracker-demo',
                                 'python_executable_name': exe.name},
                 'gaze': gaze, 'voice': bool(voice), 'raw_data': bool(raw_data),
                 'log_level': log_level, 'loops': {s['key']: s['trials'] for s in steps},
                 'eye_config': portable_eye_reference(eye_file, up),
                 'gui': gui_settings or {}}
        atomic_write(run_dir / 'gui-settings.json',
                     (json.dumps(state, ensure_ascii=False, indent=2) + '\n').encode('utf-8'), backup=False)
        atomic_write(Path(project_dir) / 'current-settings.json',
                     (json.dumps(state, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    plan = {'schema':2,'run_id':run_id,'started_at':timestamp,
            'measurement_binding':'isolated-output-v1',
            'demo_key':demo_key,'runner':RUNNERS[demo_key][0],
            'adapter':RUNNERS[demo_key][1], 'demo_root':str(root), 'upstream':str(up),
            'python':str(exe), 'eye_config':str(eye_file), 'gaze':gaze,
            'voice':bool(voice),'raw_data':bool(raw_data),'log_level':log_level,
            'steps':steps,'created_epoch':time.time(),
            'status_note':'Process success is not automatically collection or hardware validation.'}
    if project_dir is not None:
        plan['run_id'] = run_id
        plan['started_at'] = timestamp
        plan['project_name'] = Path(project_dir).name
    manifest=run_dir/'run.json'
    atomic_write(manifest,(json.dumps(plan,ensure_ascii=False,indent=2)+'\n').encode('utf-8'),backup=False)
    return manifest


def load_plan(manifest):
    path=Path(manifest).resolve()
    data=json.loads(path.read_text(encoding='utf-8'))
    if data.get('schema') != 2 or data.get('measurement_binding') != 'isolated-output-v1' or data.get('demo_key') not in RUNNERS:
        raise LaunchError('Unsupported run manifest')
    if data.get('runner') != RUNNERS[data['demo_key']][0] or data.get('adapter') != RUNNERS[data['demo_key']][1]:
        raise LaunchError('Run manifest does not match demo registry')
    demo=BY_KEY[data['demo_key']]
    if [s.get('key') for s in data['steps']] != [b.key for b in demo.blocks]:
        raise LaunchError('Run manifest block contract mismatch')
    for s in data['steps']:
        target=Path(s['config']).resolve()
        if target.parent != path.parent or not target.is_file():
            raise LaunchError('Run YAML must reside alongside the immutable manifest')
        output = Path(s['output_folder']).resolve()
        expected = (Path(s['configured_output_folder']) /
                    ('pytracker_' + path.parent.name + '_' + s['key'])).resolve()
        if output != expected or data['run_id'] != path.parent.name.rsplit('_', 1)[-1]:
            raise LaunchError('Measurement binding does not match this GUI run ID')
        try:
            config_output = str(get_value(read_source(target)[0], 'output.folder'))
        except (OSError, ValueError) as exc:
            raise LaunchError('Cannot read run YAML output folder') from exc
        if Path(config_output).resolve() != expected:
            raise LaunchError('Run YAML output folder does not match reserved session root')
    return data
