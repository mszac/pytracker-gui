"""v0.1.9: project-global state vs per-execution experiments/; no older runs/ path."""
from __future__ import annotations

import json
import os
import re
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.projects import EXPERIMENTS_DIR, ProjectStore
from pytracker_gui.runtime import prepare_run, load_plan
from pytracker_gui.runner import ExperimentRunner
from tests.test_native_launch_v015 import LauncherTest, console_log
from tests.test_gui_smoke import GuiSmoke


class ExperimentDirectoryTests(unittest.TestCase):
    setUp = LauncherTest.setUp
    _select = LauncherTest._select
    _opts = LauncherTest._opts

    def test_two_executions_share_global_project_but_not_run_files(self):
        self._select('test_en')
        project = ProjectStore(self.up / 'projects').ensure('Study_A', 'test_en')
        first = prepare_run(**self._opts(), project_dir=project, gui_settings={'language': 'pl'})
        second = prepare_run(**self._opts(), project_dir=project, gui_settings={'language': 'en'})
        self.assertEqual(EXPERIMENTS_DIR, 'experiments')
        self.assertEqual(first.parent.parent, project / 'experiments')
        self.assertEqual(second.parent.parent, project / 'experiments')
        self.assertNotEqual(first.parent, second.parent)
        self.assertFalse((project / 'runs').exists())
        self.assertTrue((project / 'project.json').is_file())
        self.assertTrue((project / 'current-settings.json').is_file())
        self.assertEqual(json.loads((project / 'current-settings.json').read_text())['gui']['language'], 'en')
        self.assertFalse((project / 'run.json').exists())
        self.assertFalse((project / 'main.yaml').exists())
        for run in (first, second):
            self.assertRegex(run.parent.name, r'^\d{8}_\d{6}_[A-Za-z0-9]{5}$')
            self.assertEqual(run_plan := load_plan(run), json.loads(run.read_text()))
            self.assertEqual(run_plan['run_id'], run.parent.name[-5:])
            self.assertTrue((run.parent / 'main.yaml').is_file())
            self.assertTrue((run.parent / 'eyetracker.yaml').is_file())
            self.assertTrue((run.parent / 'gui-settings.json').is_file())
            self.assertFalse((run.parent / 'result.json').exists())

    def test_projects_do_not_cross_store_execution_snapshots(self):
        self._select('search_en')
        project_store = ProjectStore(self.up / 'projects')
        first = project_store.ensure('First', 'search_en')
        second = project_store.ensure('Second', 'search_en')
        run = prepare_run(**self._opts(), project_dir=first)
        self.assertEqual(run.parent.parent, first / 'experiments')
        self.assertFalse((second / 'experiments').exists())
        self.assertFalse((self.up / 'projects' / 'runs').exists())

    def test_standalone_preflight_uses_new_path_without_legacy_runs_directory(self):
        self._select('test_en')
        manifest = prepare_run(**self._opts())
        self.assertEqual(manifest.parent.parent, self.base / 'appprivate' / 'experiments')
        self.assertFalse((self.base / 'appprivate' / 'runs').exists())

    def test_completed_console_log_and_result_belong_to_same_experiment(self):
        self._select('test_en')
        project = ProjectStore(self.up / 'projects').ensure('Study_C', 'test_en')
        manifest = prepare_run(**self._opts(), project_dir=project)
        runner = ExperimentRunner()
        with patch.dict(os.environ, {'PYTHONPATH': str(self.up / 'src')}):
            runner.start(manifest)
            runner._thread.join(timeout=12)
            runner._journal.wait(4)
        self.assertFalse(runner.running)
        self.assertEqual(console_log(manifest).parent, project / 'experiments' / manifest.parent.name)
        self.assertRegex(console_log(manifest).name,
                         r'^experiment_\d{8}_\d{6}_[A-Za-z0-9]{5}\.log$')
        self.assertTrue((manifest.parent / 'result.json').is_file())
        self.assertFalse((project / 'console.log').exists())


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class ExperimentDirectoryGuiTests(unittest.TestCase):
    setUp = GuiSmoke.setUp
    tearDown = GuiSmoke.tearDown

    def test_single_journal_stays_beside_its_run_configuration(self):
        from pytracker_gui.incremental_log import IncrementalExperimentLog
        project = self.gui.store.home
        run_dir = project/'experiments'/'20261011_202011_aB9z0'
        run_dir.mkdir(parents=True)
        run_file = run_dir/'run.json'
        run_file.write_text('{}')
        journal = IncrementalExperimentLog(run_dir,'aB9z0',interval=0.1)
        journal.start()
        self.gui.runner._journal = journal
        self.gui._active_manifest = run_file
        for line in ('[RUN] start\n','[STATUS] RUNNING\n',
                     '[PROCESS] exit 0\n','[FINAL] COMPLETE\n'):
            journal.append(line)
            self.gui.runner.events.put(('log',line))
        journal.finish()
        self.gui.runner.events.put(('done','COMPLETE'))
        self.gui._poll_run()
        self.assertIsNotNone(journal.wait(4))
        exported = list(run_dir.glob('experiment_*.log'))
        self.assertEqual(len(exported),1)
        self.assertFalse(list(run_dir.glob('console_*.log')))
        self.assertEqual(exported[0].read_text('utf8'), ''.join(self.gui._run_display_lines))
        self.assertFalse((project/'runs').exists())


if __name__ == '__main__':
    unittest.main()
