"""Regression for Windows demo adapter import and full experiment log clipboard."""
from __future__ import annotations

import os
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.catalog import BY_KEY
from pytracker_gui.i18n import translate
from pytracker_gui.runtime import LaunchError, prepare_run
import tests.test_native_launch_v015 as launch_tests
import tests.test_gui_smoke as gui_tests


class AdapterPathRegression(unittest.TestCase):
    """Uses isolated fake runtime; no Tobii or PsychoPy devices are required."""
    setUp = launch_tests.LauncherTest.setUp
    _select = launch_tests.LauncherTest._select
    _opts = launch_tests.LauncherTest._opts
    _run_fake = launch_tests.LauncherTest._run_fake

    def test_adapter_loads_without_tools_init_and_with_shadowing_site_package(self):
        (self.demo_root/'tools/__init__.py').unlink()
        conflict = self.base/'foreign_packages'
        (conflict/'tools').mkdir(parents=True)
        (conflict/'tools/__init__.py').write_text(
            "raise RuntimeError('foreign tools imported instead of demo adapter')\n",encoding='utf8')
        for key, expected in (('ux_en','text'),('ux_pl','text'),
                              ('search_en','text'),('search_pl','text'),('image_en','image')):
            self._select(key)
            with patch.dict(os.environ, {'PYTHONPATH':str(conflict)}):
                manifest, _runner = self._run_fake()
            log=launch_tests.console_log(manifest).read_text(encoding='utf8')
            self.assertIn('FAKE_MAIN',log)
            self.assertIn(' '+expected+'\n',log)
            self.assertIn('[ADAPTER] Loaded from ',log)
            self.assertIn(str(self.demo_root/'tools/demo_runtime_adapters.py'),log)
            self.assertIn('[ADAPTER] Applied '+expected,log)
            self.assertNotIn('foreign tools imported',log)
            self.assertIn('PROCESS COMPLETE', (manifest.parent/'result.json').read_text('utf8'))

    def test_missing_adapter_is_a_preflight_error_only_for_special_demos(self):
        (self.demo_root/'tools/demo_runtime_adapters.py').unlink()
        self._select('search_en')
        with self.assertRaisesRegex(LaunchError, 'Missing demo runtime adapter'):
            prepare_run(**self._opts())
        self._select('image_en')
        with self.assertRaisesRegex(LaunchError, 'Missing demo runtime adapter'):
            prepare_run(**self._opts())
        self._select('test_en')
        self.assertTrue(prepare_run(**self._opts()).is_file())


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name=='nt','Display required')
class ExperimentLogClipboard(unittest.TestCase):
    setUp = gui_tests.GuiSmoke.setUp
    tearDown = gui_tests.GuiSmoke.tearDown
    def _buttons(self, widget):
        result=[]
        for child in widget.winfo_children():
            if isinstance(child, tk.Button): result.append(child)
            try:
                import tkinter.ttk as ttk
                if isinstance(child, ttk.Button): result.append(child)
            except ImportError:
                pass
            result.extend(self._buttons(child))
        return result

    def test_copy_entire_visible_log_and_restore_after_reopen(self):
        self.gui._show_run_console()
        self.gui._append_run_log('[RUN] run.json\n')
        self.gui._append_run_log('[STATUS] RUNNING: Text Search EN\n')
        self.gui._append_run_log('Traceback example: no adapter\n')
        self.gui._append_run_log('[FINAL] FAILED: main, exit 1\n')
        expected=self.gui.run_log.get('1.0','end-1c')
        self.assertEqual(expected,''.join(self.gui._run_display_lines))
        buttons=self._buttons(self.gui.run_console)
        copy_button=next(b for b in buttons if b.cget('text')=='Kopiuj cały log')
        copy_button.invoke()
        self.assertEqual(self.root.clipboard_get(),expected)
        self.gui.run_console.destroy()
        self.root.update()
        self.gui._append_run_log('[REOPEN] Still available\n')
        self.gui._show_run_console()
        self.assertEqual(self.gui.run_log.get('1.0','end-1c'),expected+'[REOPEN] Still available\n')
        self.gui._copy_run_log()
        self.assertEqual(self.root.clipboard_get(),expected+'[REOPEN] Still available\n')
        self.assertIn('Skopiowano',self.gui.status.get())

    def test_log_copy_button_english_translation(self):
        self.gui.language_name.set('English')
        self.gui._on_language_changed()
        self.gui._show_run_console()
        texts={b.cget('text') for b in self._buttons(self.gui.run_console)}
        self.assertIn('Copy entire log',texts)
        self.assertEqual(translate('Kopiuj cały log','pl'),'Kopiuj cały log')
        self.assertEqual(translate('Kopiuj cały log','en'),'Copy entire log')


if __name__=='__main__':
    unittest.main()
