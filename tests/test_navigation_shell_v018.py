"""v0.1.8 navigation contract: lazy views and unchanged experiment ownership."""
import os
import shutil
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.shell import AppShell, SCREEN_IDS
from pytracker_gui.storage import save_settings

FIXTURES = Path(__file__).parent / 'fixtures' / 'examples'


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class NavigationShellTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name)
        upstream = self.home / 'tobii-pytracker'
        demo_root = upstream / 'tobii-pytracker-demo'
        (upstream / 'src/tobii_pytracker').mkdir(parents=True)
        (upstream / 'configs').mkdir()
        (upstream / 'configs/mouse_eyetracker_config.yaml').write_text('mouse: true\n')
        (upstream / 'configs/eyetracker_config.yaml').write_text('device: true\n')
        (upstream / 'pyproject.toml').write_text('[build-system]\n')
        shutil.copytree(FIXTURES, demo_root / 'examples')
        (demo_root / 'tools').mkdir()
        (demo_root / 'tools/run-demo.sh').write_text('#!/bin/bash\n')
        save_settings(self.home, {'demo_root': str(demo_root), 'upstream_root': str(upstream)})
        self.root = tk.Tk()
        self.root.withdraw()
        self.shell = AppShell(self.root, home=self.home)
        self.gui = self.shell.experiment
        self.root.update()

    def tearDown(self):
        if self.root.winfo_exists():
            self.root.destroy()
        self.temp.cleanup()

    def test_lazy_creation_and_reuse_of_independent_screens(self):
        self.assertEqual(self.shell.created_screens, ('experiment',))
        self.assertEqual(self.shell.current_screen, 'experiment')
        self.assertIs(self.gui.master, self.shell.host)
        self.assertEqual(len(self.gui.pages), 6)
        for key in ('logs', 'statistics', 'manual', 'gui-settings'):
            self.shell.select_screen(key)
            self.root.update()
            current = self.shell._screens[key]
            self.assertTrue(current.winfo_manager())
            self.shell.select_screen('experiment')
            self.root.update()
            self.assertIs(self.gui, self.shell._screens['experiment'])
            self.shell.select_screen(key)
            self.assertIs(current, self.shell._screens[key])
        self.assertEqual(set(self.shell.created_screens), set(SCREEN_IDS))
        with self.assertRaises(ValueError):
            self.shell.select_screen('unknown')

    def test_invalid_unsaved_yaml_survives_navigation_without_commit_or_disk_io(self):
        self.gui.tabs.select(self.gui.pages['YAML'])
        self.root.update()
        self.gui.yaml_editor.delete('1.0', 'end')
        self.gui.yaml_editor.insert('1.0', 'invalid: [unfinished')
        self.gui.raw_dirty = True
        current = self.gui.yaml_editor
        with patch.object(self.gui, '_commit_tab', side_effect=AssertionError('Must not commit')), \
             patch.object(self.gui.store, 'save', side_effect=AssertionError('Must not save')):
            self.shell.select_screen('logs')
            self.shell.select_screen('experiment')
            self.assertIs(self.gui.yaml_editor, current)
            self.assertEqual(self.gui.yaml_editor.get('1.0', 'end-1c'), 'invalid: [unfinished')
            self.assertTrue(self.gui.raw_dirty)
            self.assertEqual(self.gui.active_tab, 'YAML')

    def test_running_session_ownership_and_project_context_unchanged(self):
        self.assertTrue(self.gui.loaded)
        initial_demo = self.gui.demo.key
        initial_project = self.gui._active_project
        self.assertIn(initial_project, self.shell.project_context.get())
        with patch.object(type(self.gui.runner), 'running', property(lambda _self: True)), \
             patch.object(self.gui.runner, 'stop', side_effect=AssertionError('Unexpected stop')), \
             patch.object(self.gui.runner, 'start', side_effect=AssertionError('Unexpected start')), \
             patch.object(self.gui, '_refresh_all', side_effect=AssertionError('Unexpected rebuild')):
            self.shell.select_screen('logs')
            self.shell.select_screen('statistics')
            self.shell.select_screen('experiment')
        self.assertEqual(self.gui.demo.key, initial_demo)
        self.assertEqual(self.gui._active_project, initial_project)
        self.assertEqual(self.gui.gaze.get(), 'mouse')

    def test_language_switch_updates_navigation_and_lazy_views(self):
        self.assertEqual(self.shell.nav_buttons['experiment'].cget('text'), 'Eksperyment')
        self.gui.language_name.set('English')
        self.gui._on_language_changed()
        self.assertEqual(self.shell.nav_buttons['experiment'].cget('text'), 'Experiment')
        self.assertEqual(self.shell.nav_buttons['logs'].cget('text'), 'Logs')
        self.shell.select_screen('logs')
        log_screen = self.shell._screens['logs']
        self.assertEqual(log_screen.title_label.cget('text'), 'Experiment logs')
        self.gui.language_name.set('Polski')
        self.gui._on_language_changed()
        self.assertEqual(self.shell.nav_buttons['statistics'].cget('text'), 'Statystyki')
        self.assertEqual(log_screen.title_label.cget('text'), 'Logi eksperymentów')
        self.assertIn('Projekt:', self.shell.project_context.get())

    def test_close_is_delegated_and_no_idle_tasks_are_scheduled_by_switching(self):
        # Existing editor owns close safeguards; the shell adds none.
        with patch.object(self.gui, 'request_close', return_value='delegated') as close:
            self.assertEqual(self.shell.request_close(), 'delegated')
            close.assert_called_once_with()
        with patch.object(self.root, 'after', side_effect=AssertionError('Unexpected timer')):
            self.shell.select_screen('logs')
            self.shell.select_screen('logs')
            self.shell.select_screen('statistics')
            self.shell.select_screen('experiment')


if __name__ == '__main__':
    unittest.main()
