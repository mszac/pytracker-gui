"""Auto-log display can be disabled without losing archival output (no real PsychoPy)."""
import os
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.test_gui_smoke import GuiSmoke
from pytracker_gui.i18n import translate
from pytracker_gui.storage import load_settings


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class AutoShowLogsTests(unittest.TestCase):
    setUp = GuiSmoke.setUp
    tearDown = GuiSmoke.tearDown
    def test_default_on_and_persisted_off(self):
        self.assertTrue(self.gui.auto_show_logs.get())
        self.gui.tabs.select(self.gui.pages['Uruchomienie'])
        self.root.update()
        self.assertEqual(self.gui.auto_show_toggle.cget('text'), 'Automatycznie pokazuj logi')
        self.gui.auto_show_toggle.invoke()
        self.assertFalse(self.gui.auto_show_logs.get())
        self.assertIs(load_settings(self.home)['auto_show_logs'], False)
        self.gui.destroy()
        # User setting remains in app-private settings.json, not in project YAML.
        from pytracker_gui.app import PytrackerGUI
        self.gui = PytrackerGUI(self.root, home=self.home)
        self.root.update()
        self.assertFalse(self.gui.auto_show_logs.get())
        self.gui.language_name.set('English')
        self.gui._on_language_changed()
        self.gui.tabs.select(self.gui.pages['Uruchomienie'])
        self.root.update()
        self.assertEqual(self.gui.auto_show_toggle.cget('text'), 'Auto-show logs')
        self.assertEqual(translate('Automatycznie pokazuj logi', 'en'), 'Auto-show logs')

    def _fake_start(self, *, auto):
        self.gui.auto_show_logs.set(auto)
        run_dir = self.home / 'projects' / 'test_en' / 'experiments' / '20261011_230000_Q1aB2'
        run_dir.mkdir(parents=True, exist_ok=True)
        manifest = run_dir / 'run.json'
        manifest.write_text('{}', encoding='utf-8')
        with patch('pytracker_gui.app.probe_interpreter', return_value={
            'version': [3, 10, 0], 'modules': {'psychopy': 'installed', 'tobii_pytracker': 'installed'}}), \
             patch('pytracker_gui.app.prepare_run', return_value=manifest), \
             patch.object(self.gui.store, 'save'), \
             patch.object(self.gui.runner, 'start'), \
             patch.object(self.gui, '_poll_run'):
            self.gui._start_run()
        self.assertEqual(self.gui._active_manifest, manifest)
        return manifest

    def test_off_has_no_auto_window_and_bounded_preview_copy(self):
        manifest = self._fake_start(auto=False)
        self.assertTrue(self.gui.run_console is None or not self.gui.run_console.winfo_exists())
        self.gui._append_run_log('[STATUS] RUNNING\n')
        for _ in range(2300):
            self.gui._append_run_log('Line ' + ('abcde'*30) + '\n')
        self.assertLessEqual(len(self.gui._run_display_lines), 2000)
        self.assertLessEqual(sum(map(len, self.gui._run_display_lines)), 262144)
        self.assertIsNotNone(self.gui._run_spool)
        self.assertTrue(self.gui._run_spool._rolled)
        self.gui._append_run_log('[FINAL] COMPLETE\n')
        self.gui._save_finished_experiment_log()
        # GUI never creates a second persistent log; runner owns the journal.
        self.assertFalse(list(manifest.parent.glob('experiment_*.log')))
        self.gui._show_run_console()
        self.assertTrue(self.gui.run_console.winfo_exists())
        self.assertLessEqual(len(self.gui.run_log.get('1.0','end-1c')), 262144)
        self.gui._copy_run_log()
        copied=self.root.clipboard_get()
        self.assertEqual(copied.count('Line abcde'),2300)
        self.assertTrue(copied.endswith('[FINAL] COMPLETE\n'))

    def test_spool_failure_is_nonfatal_and_not_retried_per_line(self):
        self.gui.auto_show_logs.set(False)
        with patch('pytracker_gui.app.tempfile.SpooledTemporaryFile', side_effect=OSError('temp unavailable')) as create:
            for i in range(50):
                self.gui._append_run_log('line '+str(i)+'\n')
        self.assertEqual(create.call_count, 1)
        self.assertEqual(len(self.gui._run_display_lines), 50)
        self.assertTrue(self.gui._run_spool_failed)

    def test_on_opens_and_opt_out_closes_and_stops_rendering(self):
        self._fake_start(auto=True)
        self.assertTrue(self.gui.run_console.winfo_exists())
        self.gui.tabs.select(self.gui.pages['Uruchomienie'])
        self.root.update()
        # Switching to OFF closes a currently visible log viewer.
        self.gui.auto_show_toggle.invoke()
        self.assertFalse(self.gui.auto_show_logs.get())
        self.assertFalse(self.gui.run_console.winfo_exists())
        self.gui._append_run_log('Off means no Tk console widget\n')
        self.assertIsNone(self.gui.run_log)
        self.assertIn('Off means', ''.join(self.gui._run_display_lines))
        self.gui._save_finished_experiment_log()
        self.assertFalse(list((self.home/'projects/test_en/experiments/20261011_230000_Q1aB2').glob('experiment_*.log')))

if __name__ == '__main__':
    unittest.main()
