"""One experiment block per native subprocess, mirroring original demo lifecycle.

Must be invoked with the selected research Python 3.10, not imported by Tkinter.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import time
from pathlib import Path

from .runtime import load_plan, find_exact_session


def _collection_validator(plan, block, started):
    """Validate only the session in the run-ID-specific reserved output root."""
    session, reason = find_exact_session(block)
    if session is None:
        print('[SESSION] UNRESOLVED: run_id=' + plan['run_id'] +
              ' block=' + block['key'] + ' ' + reason, flush=True)
        if block['validator_eligible']:
            print('[COLLECTION] FAILED: cannot establish unique session binding',flush=True)
            return 1
        print('[COLLECTION] NOT VERIFIED: unique session binding unavailable',flush=True)
        return 0
    print('[SESSION] BOUND: run_id=' + plan['run_id'] +
          ' block=' + block['key'] + ' data_csv=' + str(session / 'data.csv'), flush=True)
    if not block['validator_eligible']:
        print('[COLLECTION] NOT VERIFIED: no gaze, partial session or modified source dataset/output layout',flush=True)
        return 0
    demo = plan['runner']
    script = Path(plan['demo_root'])/'examples'/demo/'validate_collection.py'
    if not script.is_file():
        print('[COLLECTION] NOT VERIFIED: original validator absent',flush=True)
        return 0
    root = block['output_folder']
    if demo == 'timeseries_noise_demo':
        args=['--domain',block['key'],'--session',str(session)]
    elif demo == 'test_demo':
        # This validator has no --session switch. Its --output-root contains
        # exactly one candidate, and we have already checked that constraint.
        args=['--output-root',root]
    else:
        args=['--session',str(session)]
        if demo in ('ux_ab_demo','text_search_demo'):
            args += ['--dataset',block['dataset_path']]
    print('[COLLECTION] Invoking demo repository validator',flush=True)
    result=subprocess.run([plan['python'],str(script),*args], cwd=plan['demo_root'],check=False)
    if result.returncode:
        print('[COLLECTION] FAILED: exit code',result.returncode,flush=True)
    else:
        print('[COLLECTION] PASS: validator for this block',flush=True)
    return result.returncode



def load_demo_adapter(demo_root, kind):
    """Load the selected checkout's adapter by path, not an ambiguous ``tools`` package.

    In particular, ``tools/`` has no mandatory __init__.py in the original
    demo repo. A third-party ``tools`` package can therefore shadow it on
    Windows/Python environments even with the correct child working directory.
    """
    if kind not in ('text', 'image'):
        raise ValueError('Unsupported demo adapter: ' + repr(kind))
    adapter_file = (Path(demo_root).resolve() / 'tools' / 'demo_runtime_adapters.py')
    if not adapter_file.is_file():
        raise FileNotFoundError(
            'Missing demo adapter: ' + str(adapter_file) +
            '. Update or restore the original tobii-pytracker-demo checkout.'
        )
    spec = importlib.util.spec_from_file_location('_pytracker_selected_demo_adapters', adapter_file)
    if spec is None or spec.loader is None:
        raise ImportError('Cannot load the demo adapter from: ' + str(adapter_file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    install_name = ('install_text_demo' if kind == 'text' else 'install_image_semantic_demo')
    install = getattr(module, install_name)
    print('[ADAPTER] Loaded from ' + str(adapter_file), flush=True)
    return install


def run_block(manifest, key):
    plan=load_plan(manifest)
    matches=[s for s in plan['steps'] if s['key']==key]
    if len(matches)!=1:
        raise ValueError('Unknown block')
    block=matches[0]
    print('[RUN] demo=',plan['demo_key'],'block=',key,'gaze=',plan['gaze'],flush=True)
    # Imports intentionally deferred until AFTER GUI has spawned the native child.
    from tobii_pytracker import main as main_module
    from tobii_pytracker.configs.custom_config import CustomConfig
    from tobii_pytracker.utils.custom_logger import CustomLogger
    if plan['adapter']:
        install = load_demo_adapter(plan['demo_root'], plan['adapter'])
        install(main_module)
        print('[ADAPTER] Applied ' + plan['adapter'] + ' adapter', flush=True)
    main_module.LOGGER = CustomLogger(plan['log_level'], main_module.__name__).logger
    started=time.time()
    print('[RUN] PsychoPy runtime starting',flush=True)
    main_module.main(
        config=CustomConfig(block['config']), loop_count=block['trials'],
        eyetracker_config_file=plan['eye_config'],
        enable_eyetracker=plan['gaze']!='none',enable_voice=plan['voice'],
        raw_data=plan['raw_data'],enable_psychopy=True,
    )
    print('[RUN] PsychoPy main returned normally',flush=True)
    return _collection_validator(plan,block,started)


def main(argv=None):
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('manifest')
    parser.add_argument('block')
    args=parser.parse_args(argv)
    try:
        return run_block(args.manifest,args.block)
    except Exception:
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
