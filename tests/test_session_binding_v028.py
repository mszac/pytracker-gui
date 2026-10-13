"""Explicit GUI run-ID → exactly one native measurement session mapping tests."""
from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from .test_native_launch_v015 import LauncherTest
from pytracker_gui.launch_child import _collection_validator
from pytracker_gui.runtime import find_exact_session, load_plan, prepare_run, session_binding
from pytracker_gui.yamlconfig import get_value, read_source


class SessionBindingTest(LauncherTest):
    """Use a fake repo/process; do not load PsychoPy or any real tracker."""

    def test_run_id_in_output_and_snapshot_for_each_block(self):
        self._select('ts_machine_pv')
        manifest = prepare_run(**self._opts())
        plan = load_plan(manifest)
        self.assertRegex(plan['run_id'], r'^[A-Za-z0-9]{5}$')
        self.assertEqual(manifest.parent.name[-5:], plan['run_id'])
        roots = [step['output_folder'] for step in plan['steps']]
        self.assertEqual(len(roots), len(set(roots)))
        for step in plan['steps']:
            self.assertIn(manifest.parent.name, Path(step['output_folder']).name)
            self.assertTrue(Path(step['output_folder']).is_dir())
            self.assertEqual(get_value(read_source(Path(step['config']))[0], 'output.folder'), step['output_folder'])
            self.assertNotEqual(step['output_folder'], step['configured_output_folder'])

    def test_exact_session_and_result_json_association(self):
        self._select('test_en')
        manifest = prepare_run(**self._opts())
        plan = load_plan(manifest)
        step = plan['steps'][0]
        # A foreign, more recent session must never be considered.
        foreign = Path(step['configured_output_folder']) / 'another_users_session'
        foreign.mkdir(parents=True)
        (foreign/'data.csv').write_text('foreign',encoding='utf8')
        ours = Path(step['output_folder']) / 'native_timestamp'
        ours.mkdir()
        (ours/'data.csv').write_text('own',encoding='utf8')
        session, why = find_exact_session(step)
        self.assertEqual(session, ours.resolve())
        self.assertIsNone(why)
        details = session_binding(step)
        self.assertEqual(details['data_csv'], str((ours/'data.csv').resolve()))
        from pytracker_gui.runner import ExperimentRunner
        ExperimentRunner()._save_result(manifest, 'PROCESS COMPLETE — COLLECTION NOT VERIFIED')
        result = json.loads((manifest.parent/'result.json').read_text(encoding='utf8'))
        self.assertEqual(result['run_id'], plan['run_id'])
        self.assertEqual(result['measurement_sessions']['main']['state'], 'linked')
        self.assertEqual(result['measurement_sessions']['main']['data_csv'], str((ours/'data.csv').resolve()))
        self.assertNotIn('another_users_session', json.dumps(result))

    def test_no_candidate_and_multiple_candidates_fail_closed(self):
        self._select('test_en')
        manifest = prepare_run(**self._opts())
        plan = load_plan(manifest)
        step = dict(plan['steps'][0], validator_eligible=True)
        session, reason = find_exact_session(step)
        self.assertIsNone(session)
        self.assertIn('found 0', reason)
        self.assertEqual(_collection_validator(plan, step, 0), 1)
        for index in range(2):
            path = Path(step['output_folder']) / f'session_{index}'
            path.mkdir()
            (path/'data.csv').write_text('sample',encoding='utf8')
        session, reason = find_exact_session(step)
        self.assertIsNone(session)
        self.assertIn('found 2', reason)
        self.assertEqual(_collection_validator(plan, step, 0), 1)

    def test_validator_uses_explicit_session_in_non_test_projects(self):
        self._select('search_en')
        manifest = prepare_run(**self._opts())
        plan = load_plan(manifest)
        step = dict(plan['steps'][0], validator_eligible=True)
        session = Path(step['output_folder'])/'created_by_native'
        session.mkdir()
        (session/'data.csv').write_text('sample',encoding='utf8')
        script = self.demo_root/'examples'/plan['runner']/'validate_collection.py'
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text('pass\n',encoding='utf8')
        with patch('pytracker_gui.launch_child.subprocess.run', return_value=subprocess.CompletedProcess([],0)) as run:
            self.assertEqual(_collection_validator(plan, step, 0), 0)
        argv = run.call_args.args[0]
        self.assertEqual(argv[argv.index('--session')+1], str(session.resolve()))
        self.assertNotIn('--started-at', argv)
        self.assertNotIn('--output-root', argv)

    def test_full_fake_child_writes_measurement_in_run_id_folder(self):
        self._select('test_en')
        fake = self.up/'src/tobii_pytracker/main.py'
        fake.write_text('''from pathlib import Path
from ruamel.yaml import YAML
LOGGER=None
def main(**kwargs):
    config = YAML(typ="safe").load(Path(kwargs["config"].config_file).read_text(encoding="utf8"))
    output = Path(config["output"]["folder"]) / "native_session"
    output.mkdir(parents=True, exist_ok=False)
    (output / "data.csv").write_text("header\\nmeasurement\\n", encoding="utf8")
    print("FAKE_NATIVE_MEASUREMENT=" + str(output / "data.csv"), flush=True)
''',encoding='utf8')
        manifest, runner = self._run_fake()
        plan = load_plan(manifest)
        measured = Path(plan['steps'][0]['output_folder'])/'native_session'/'data.csv'
        self.assertTrue(measured.is_file())
        result = json.loads((manifest.parent/'result.json').read_text(encoding='utf8'))
        self.assertEqual(result['run_id'], plan['run_id'])
        self.assertEqual(result['measurement_sessions']['main']['data_csv'], str(measured.resolve()))
        self.assertEqual(result['measurement_sessions']['main']['state'], 'linked')
        self.assertIn('COLLECTION NOT VERIFIED',result['status'])

    def test_test_demo_validator_is_confined_to_unique_root(self):
        self._select('test_en')
        manifest = prepare_run(**self._opts())
        plan = load_plan(manifest)
        step = dict(plan['steps'][0], validator_eligible=True)
        session = Path(step['output_folder'])/'created_by_native'
        session.mkdir()
        (session/'data.csv').write_text('sample', encoding='utf8')
        script = self.demo_root/'examples'/plan['runner']/'validate_collection.py'
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text('pass\n',encoding='utf8')
        with patch('pytracker_gui.launch_child.subprocess.run', return_value=subprocess.CompletedProcess([],0)) as run:
            self.assertEqual(_collection_validator(plan, step, 0), 0)
        argv = run.call_args.args[0]
        self.assertEqual(argv[argv.index('--output-root')+1], step['output_folder'])
        self.assertNotIn('--min-mtime', argv)
