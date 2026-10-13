"""v0.2.1: branding, lazy tile chooser, brighter icons, selected-tab spacing."""
import os
import unittest
from pathlib import Path
from tkinter import ttk
from unittest.mock import patch

from pytracker_gui.theme import COLORS, icon
from tests import test_navigation_shell_v018 as navigation_suite


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class DashboardVisualTests(unittest.TestCase):
    setUp = navigation_suite.NavigationShellTests.setUp
    tearDown = navigation_suite.NavigationShellTests.tearDown

    def test_home_created_only_after_click_and_not_by_startup(self):
        self.assertEqual(self.shell.created_screens, ('experiment',))
        self.assertTrue(self.shell.brand_logo_label.cget('image'))
        self.assertEqual(self.shell.brand_button.cget('text'), 'pytracker-gui')
        with patch.object(self.root, 'after', side_effect=AssertionError('Navigation timer')), \
             patch.object(self.gui.runner, 'start', side_effect=AssertionError('Unexpected start')), \
             patch.object(self.gui.runner, 'stop', side_effect=AssertionError('Unexpected stop')):
            self.shell.brand_button.invoke()
            self.assertEqual(self.shell.current_screen, 'home')
            self.assertEqual(self.shell.created_screens, ('experiment', 'home'))
            home = self.shell._screens['home']
            self.shell.brand_button.invoke()
            self.assertIs(self.shell._screens['home'], home)
            self.assertEqual(len(home.tile_buttons), 4)
            home.tile_buttons['logs'].invoke()
            self.assertEqual(self.shell.current_screen, 'logs')
            self.shell.brand_button.invoke()
            self.assertIs(self.shell._screens['home'], home)
            home.tile_buttons['experiment'].invoke()
            self.assertIs(self.shell._screens['experiment'], self.gui)

    def test_unsaved_invalid_yaml_is_not_committed_or_changed_via_home_tiles(self):
        self.gui.tabs.select(self.gui.pages['YAML'])
        self.root.update()
        self.gui.yaml_editor.delete('1.0', 'end')
        self.gui.yaml_editor.insert('1.0', 'unterminated: [')
        self.gui.raw_dirty = True
        with patch.object(self.gui, '_commit_tab', side_effect=AssertionError('No commit')), \
             patch.object(self.gui.store, 'save', side_effect=AssertionError('No save')):
            self.shell.open_home()
            self.shell._screens['home'].tile_buttons['experiment'].invoke()
        self.assertEqual(self.gui.yaml_editor.get('1.0', 'end-1c'), 'unterminated: [')
        self.assertTrue(self.gui.raw_dirty)

    def test_dashboard_language_and_project_context(self):
        self.shell.open_home()
        home = self.shell._screens['home']
        self.assertEqual(home.title_label.cget('text'), 'Wybierz ekran')
        self.gui.language_name.set('English')
        self.gui._on_language_changed()
        self.assertEqual(home.title_label.cget('text'), 'Choose a screen')
        self.assertEqual(home.tile_buttons['manual'].cget('text'), 'Manual')
        self.assertIn(self.gui.project_name.get(), self.shell.project_context.get())
        home.tile_buttons['statistics'].invoke()
        self.assertEqual(self.shell.current_screen, 'statistics')

    def test_bright_accent_only_selected_tab_inset_halved_and_high_res_icons(self):
        s = ttk.Style(self.root)
        self.assertEqual(COLORS['accent'], '#ff9d45')
        self.assertEqual(tuple(s.configure('TNotebook.Tab')['padding']), (12, 9))
        self.assertIn(('selected', (6, 9)), [(state, tuple(pad)) for state, pad in s.map('TNotebook.Tab')['padding']])
        self.assertEqual(s.lookup('Brand.TButton', 'font'), 'Segoe UI 17 bold' if os.name == 'nt' else s.lookup('Brand.TButton', 'font'))
        self.assertEqual(s.lookup('Accent.TButton', 'font'), 'TkDefaultFont 10 bold')
        self.assertEqual(icon(self.root, 'logs').width(), 40)
        self.assertEqual(icon(self.root, 'logs').height(), 40)
        self.assertIs(icon(self.root, 'logs'), icon(self.root, 'logs'))
        assets = Path(__file__).resolve().parents[1] / 'pytracker_gui' / 'assets'
        self.assertEqual(len([p for p in assets.glob('*.png') if not p.name.startswith('dashboard-')]), 52)
        self.assertLess(sum(p.stat().st_size for p in assets.glob('*.png')
                            if not p.name.startswith('dashboard-')), 450000)

if __name__ == '__main__':
    unittest.main()
