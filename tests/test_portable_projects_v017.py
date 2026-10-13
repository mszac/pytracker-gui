"""Project isolation, portable state, post-run-only logs; no real PsychoPy required."""
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import tkinter as tk
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.projects import ProjectStore, ProjectError
from pytracker_gui.profiles import ProfileStore
from pytracker_gui.runner import ExperimentRunner
from pytracker_gui.runtime import prepare_run
from pytracker_gui.yamlconfig import dump_doc, read_source
from tests.test_native_launch_v015 import LauncherTest, console_log
from tests.test_gui_smoke import GuiSmoke


class ProjectStorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.projects = ProjectStore(self.root / 'projects')

    def test_names_and_restricted_paths(self):
        for bad in ('../bad', '..', '.hidden', 'a/b', 'a\\b', 'a:b', 'x'*65, '', ' name '):
            with self.assertRaises(ProjectError):
                self.projects.ensure(bad, 'test_en')
        directory = self.projects.ensure('Study_A-12', 'test_en')
        self.assertEqual(self.projects.ensure('Study_A-12', 'test_en'), directory)
        self.assertEqual(self.projects.projects_for('test_en'), ['Study_A-12'])
        self.assertEqual(self.projects.projects_for('search_en'), [])
        with self.assertRaises(ProjectError):
            self.projects.ensure('Study_A-12', 'search_en')

    def test_relocated_project_rebinds_iohub(self):
        for version in ('old', 'new'):
            (self.root/version/'configs').mkdir(parents=True)
            (self.root/version/'configs/mouse_eyetracker_config.yaml').write_text('mouse: true\n')
        original = self.projects.ensure('Portable', 'test_en')
        docs = {'main':'dataset:\n  image:\n    path: images\n'}
        store = ProfileStore(original, upstream=self.root/'old')
        store.save('test_en',docs,{'main':'abc'},'mouse',str(self.root/'old/configs/mouse_eyetracker_config.yaml'))
        copied = self.root/'other-machine'/'projects'/'Portable'
        copied.parent.mkdir(parents=True)
        shutil.copytree(original,copied)
        new_store = ProfileStore(copied, upstream=self.root/'new')
        saved, meta, _ = new_store.load('test_en',{'main':'abc'})
        self.assertEqual(saved, docs)
        self.assertEqual(meta['eye_config'],str((self.root/'new/configs/mouse_eyetracker_config.yaml').resolve()))
        self.assertNotIn('old', str(meta['eye_config']))


class RunProjectTests(unittest.TestCase):
    setUp = LauncherTest.setUp
    _select = LauncherTest._select
    _opts = LauncherTest._opts
    def test_five_character_id_and_portable_run_files(self):
        self._select('test_en')
        project = ProjectStore(self.up/'projects').ensure('Research_1', 'test_en')
        args = self._opts()
        run_1=prepare_run(**args, project_dir=project, gui_settings={'language':'en'})
        run_2=prepare_run(**args, project_dir=project, gui_settings={'language':'pl'})
        for manifest in (run_1,run_2):
            self.assertRegex(manifest.parent.name,r'^\d{8}_\d{6}_[A-Za-z0-9]{5}$')
            plan=json.loads(manifest.read_text(encoding='utf8'))
            self.assertEqual(plan['run_id'],manifest.parent.name[-5:])
            self.assertEqual(plan['project_name'],'Research_1')
            self.assertEqual((manifest.parent/'eyetracker.yaml').read_text(),
                             (self.up/'configs/mouse_eyetracker_config.yaml').read_text())
            self.assertTrue((manifest.parent/'main.yaml').is_file())
            state=json.loads((manifest.parent/'gui-settings.json').read_text(encoding='utf8'))
            self.assertEqual(state['eye_config']['base'],'upstream')
            self.assertEqual(state['eye_config']['path'],'configs/mouse_eyetracker_config.yaml')
            self.assertNotIn(str(self.up), (manifest.parent/'gui-settings.json').read_text(encoding='utf8'))
        self.assertNotEqual(run_1,run_2)
        self.assertEqual(json.loads((project/'current-settings.json').read_text(encoding='utf8'))['gui']['language'],'pl')

    def test_raw_console_persisted_only_after_child_finishes(self):
        self._select('test_en')
        project = ProjectStore(self.up/'projects').ensure('Research_2','test_en')
        manifest=prepare_run(**self._opts(),project_dir=project)
        runner=ExperimentRunner()
        with patch.dict(os.environ, {'PYTHONPATH':str(self.up/'src'), 'FAKE_BLOCK_SLEEP':'1'}):
            runner.start(manifest)
            for _ in range(120):
                if runner._proc is not None:
                    break
                time.sleep(.02)
            self.assertTrue(runner.running)
            self.assertFalse(list(manifest.parent.glob('experiment_*.log')))
            self.assertLessEqual(len(list(manifest.parent.glob('experiment_*.log.part'))), 1)
            runner.stop(wait=True)
            runner._thread.join(timeout=7)
            runner._journal.wait(4)
        self.assertFalse(runner.running)
        self.assertRegex(console_log(manifest).name, r'^experiment_\d{8}_\d{6}_[A-Za-z0-9]{5}\.log\.part$')
        self.assertIn('[LOG] INTERRUPTED',console_log(manifest).read_text('utf8'))
        self.assertIn('CANCELLED',(manifest.parent/'result.json').read_text(encoding='utf8'))


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name=='nt','Requires display')
class ProjectGuiTests(unittest.TestCase):
    setUp = GuiSmoke.setUp
    tearDown = GuiSmoke.tearDown
    def test_independent_gui_projects_same_variant(self):
        self.assertEqual(self.gui.project_name.get(),'test_en')
        self.gui.gaze.set('none')
        self.assertTrue(self.gui._save())
        self.gui.projects.ensure('Copied-Study','test_en')
        self.gui.project_name.set('Copied-Study')
        self.gui._project_changed()
        self.assertEqual(self.gui.project_name.get(),'Copied-Study')
        self.assertEqual(self.gui.gaze.get(),'mouse')
        self.gui.gaze.set('tobii')
        self.assertTrue(self.gui._save())
        self.gui.project_name.set('test_en')
        self.gui._project_changed()
        self.assertEqual(self.gui.gaze.get(),'none')
        self.assertTrue((self.home/'projects/Copied-Study/profiles/test_en/main.yaml').exists())

    def test_gui_done_does_not_write_second_log(self):
        from pytracker_gui.incremental_log import IncrementalExperimentLog
        run_dir = self.gui.store.home/'experiments'/'20261011_171201_aB9z0'
        run_dir.mkdir(parents=True)
        manifest = run_dir/'run.json'
        manifest.write_text('{}')
        journal = IncrementalExperimentLog(run_dir,'aB9z0',interval=0.1)
        journal.start()
        self.gui.runner._journal = journal
        self.gui._active_manifest = manifest
        for line in ('[RUN] '+str(manifest)+'\n','[STATUS] RUNNING\n',
                     'Experiment line\n','[FINAL] PROCESS COMPLETE\n'):
            journal.append(line)
            self.gui.runner.events.put(('log', line))
        journal.finish()
        self.gui.runner.events.put(('done','PROCESS COMPLETE'))
        self.gui._poll_run()
        self.assertIsNotNone(journal.wait(4))
        logs = list(run_dir.glob('experiment_*.log'))
        self.assertEqual(len(logs),1)
        self.assertFalse(list(run_dir.glob('console_*.log')))
        self.assertIn('[STATUS] RUNNING',logs[0].read_text('utf8'))
        self.assertIn('[FINAL] PROCESS COMPLETE',logs[0].read_text('utf8'))
        self.assertTrue((self.home/'projects/test_en/project.json').is_file())

    def test_imports_legacy_profile_by_copy_only_for_default_project(self):
        from pytracker_gui.profiles import ProfileStore
        original = self.home / 'profiles'
        legacy_store = ProfileStore(self.home)
        contents = {k: dump_doc(v) for k, v in self.gui.docs.items()}
        legacy_store.save(self.gui.demo.key, contents, self.gui.hashes, 'none', self.gui.eye.get())
        legacy_bytes = (original / 'test_en' / 'main.yaml').read_bytes()
        # Simulate upgrading from the old app-private profile after the new
        # project tree was first discovered; do not overwrite an existing user profile.
        latest = self.home / 'projects' / 'test_en' / 'profiles' / 'test_en'
        if latest.exists():
            shutil.rmtree(latest)
        self.gui._activate_project('test_en', 'test_en')
        self.assertEqual((latest / 'main.yaml').read_bytes(), legacy_bytes)
        self.assertEqual((original / 'test_en' / 'main.yaml').read_bytes(), legacy_bytes)
        other = self.gui.projects.ensure('Fresh-Study', 'test_en')
        self.gui._activate_project('test_en', 'Fresh-Study')
        self.assertFalse((other / 'profiles').exists(), 'New projects must not silently inherit the legacy profile')

    def test_gui_does_not_perform_archive_file_io_at_final(self):
        run_dir=self.gui.store.home/'experiments'/'20261011_171202_Hj4W8'
        run_dir.mkdir(parents=True)
        self.gui._active_manifest=run_dir/'run.json'
        self.gui._append_run_log('[RUN] sample\n')
        with patch('pytracker_gui.app.atomic_write',side_effect=OSError('unavailable disk')) as output:
            self.gui._save_finished_experiment_log()
        output.assert_not_called()
        self.assertIsNone(self.gui._active_manifest)



if __name__=='__main__':
    unittest.main()
