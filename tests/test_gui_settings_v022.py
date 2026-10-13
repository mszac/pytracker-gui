"""v0.2.22: only the new GUI Settings screen and approved Logs tile may change."""
import os
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch
import struct

from pytracker_gui.shell import AppShell, SCREEN_IDS
from pytracker_gui.storage import load_settings, save_settings
from pytracker_gui.screens import DashboardScreen, GuiSettingsScreen

ASSETS = Path(__file__).parents[1] / 'pytracker_gui' / 'assets'


class GuiSettingsAssetsTests(unittest.TestCase):
    def test_tile_dimensions_and_frozen_dashboard_geometry(self):
        self.assertEqual(DashboardScreen.TILE_SIZE, (546, 365))
        self.assertEqual([x[0] for x in DashboardScreen.TILES],
                         ['experiment', 'logs', 'statistics', 'manual'])
        for key, *_ in DashboardScreen.TILES:
            raw = (ASSETS / f'dashboard-{key}.png').read_bytes()[:24]
            self.assertEqual(raw[:8], b'\x89PNG\r\n\x1a\n')
            self.assertEqual(struct.unpack('>II', raw[16:24]), (546, 365))


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class GuiSettingsRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.root = tk.Tk()
        self.root.withdraw()
        self.shell = AppShell(self.root, home=self.home)
        self.root.update()

    def tearDown(self):
        if self.root.winfo_exists():
            self.root.destroy()
        self.tmp.cleanup()

    def test_lazy_screen_right_of_manual_and_paths_are_readonly(self):
        self.assertEqual(SCREEN_IDS[-2:], ('manual', 'gui-settings'))
        self.assertNotIn('gui-settings', self.shell.created_screens)
        self.shell.select_screen('gui-settings')
        page = self.shell._screens['gui-settings']
        self.assertIsInstance(page, GuiSettingsScreen)
        self.assertEqual(page.window_size_var.get(), '1429 × 1097')
        self.assertEqual(page._path_vars['gui_home'].get(), str(self.home))
        self.assertEqual(page._path_vars['projects_root'].get(), str(self.home / 'projects'))
        for var in page._path_vars.values():
            self.assertTrue(var.get())
        self.assertEqual(str(page.preset_combo.cget('state')), 'readonly')
        self.assertEqual(len(page.WINDOW_PRESETS), 5)
        self.assertIs(self.shell.experiment, self.shell._screens['experiment'])

    def test_startup_size_save_and_reload_no_yaml_or_process_actions(self):
        self.shell.select_screen('gui-settings')
        page = self.shell._screens['gui-settings']
        with patch.object(self.shell.experiment.runner, 'start', side_effect=AssertionError), \
             patch.object(self.shell.experiment.runner, 'stop', side_effect=AssertionError):
            page.window_size_var.set('1300 × 960')
            page._save()
            self.assertEqual(load_settings(self.home)['window_size'], '1300 × 960')
            self.assertEqual(self.shell.experiment.settings['window_size'], '1300 × 960')
            with self.assertRaises(ValueError):
                self.shell._save_gui_window_size('999999 × 999999')
        # The next launch uses the saved value; current geometry is not forcibly changed.
        self.root.deiconify(); self.root.update()
        self.assertIn('1429x1097', self.root.geometry())
        self.root.destroy()
        self.root = tk.Tk()
        self.root.withdraw()
        self.shell = AppShell(self.root, home=self.home)
        self.root.deiconify(); self.root.update()
        self.assertIn('1300x960', self.root.geometry())

    def test_language_refresh_and_no_extra_home_tile(self):
        self.shell.select_screen('gui-settings')
        page = self.shell._screens['gui-settings']
        page.set_language('en')
        self.assertIn('Startup', page._labels['window_size'].cget('text'))
        page.set_language('pl')
        self.assertIn('Rozmiar', page._labels['window_size'].cget('text'))
        self.shell.open_home()
        self.assertEqual(set(self.shell._screens['home'].tile_buttons),
                         {'experiment','logs','statistics','manual'})


if __name__ == '__main__':
    unittest.main()
