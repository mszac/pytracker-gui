"""v0.2.0 visual theme regression: presentation only, native Tk, no new services."""
import os
import tkinter as tk
from tkinter import ttk
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.theme import COLORS, apply_theme, icon
from pytracker_gui.help_widgets import InfoButton
from tests import test_navigation_shell_v018 as navigation_suite


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class VisualThemeTests(unittest.TestCase):
    setUp = navigation_suite.NavigationShellTests.setUp
    tearDown = navigation_suite.NavigationShellTests.tearDown

    def test_theme_is_native_static_dark_orange_without_new_runtime_dependencies(self):
        style = ttk.Style(self.root)
        self.assertEqual(style.theme_use(), 'clam')
        self.assertEqual(style.lookup('TFrame', 'background'), COLORS['surface'])
        self.assertEqual(style.lookup('Accent.TButton', 'background'), COLORS['accent'])
        self.assertEqual(self.root.cget('background'), COLORS['window'])
        self.assertEqual(self.gui.listbox.cget('background'), COLORS['field'])
        self.assertEqual(self.gui.listbox.cget('selectbackground'), COLORS['selection'])
        with patch.object(self.root, 'after', side_effect=AssertionError('theme timer')):
            apply_theme(self.root)

    def test_navigation_icons_are_cached_and_screens_still_lazy(self):
        self.assertEqual(self.shell.created_screens, ('experiment',))
        self.assertIs(icon(self.root, 'logs'), icon(self.root, 'logs'))
        self.assertIsNot(icon(self.root, 'logs'), icon(self.root, 'logs', True))
        before = self.shell.nav_buttons['logs'].cget('image')
        self.shell.select_screen('logs')
        self.assertNotEqual(before, self.shell.nav_buttons['logs'].cget('image'))
        self.assertEqual(self.shell.created_screens, ('experiment', 'logs'))
        self.shell.select_screen('experiment')
        self.assertIs(self.shell.experiment, self.shell._screens['experiment'])

    def test_tab_images_and_yaml_editor_colors_do_not_touch_unsaved_text(self):
        tabs = self.gui.tabs
        self.assertTrue(tabs.tab(self.gui.pages['Dane'], 'image'))
        tabs.select(self.gui.pages['YAML'])
        self.root.update()
        self.assertTrue(tabs.tab(self.gui.pages['YAML'], 'image'))
        self.assertEqual(self.gui.yaml_editor.cget('background'), COLORS['field'])
        self.gui.yaml_editor.insert('end', '\nNOT_A_VALID_YAML: [')
        original = self.gui.yaml_editor.get('1.0', 'end-1c')
        self.shell.select_screen('statistics')
        self.shell.select_screen('experiment')
        self.assertEqual(self.gui.yaml_editor.get('1.0', 'end-1c'), original)

    def test_help_bubble_and_user_language_survive_dark_theme(self):
        def walk(root):
            for child in root.winfo_children():
                if isinstance(child, InfoButton):
                    yield child
                yield from walk(child)
        button = next(child for child in walk(self.gui.pages['Monitor'])
                      if child.help_key == 'display.monitor.width')
        button.invoke()
        self.assertTrue(self.gui.info_popover.popup.winfo_exists())
        self.assertEqual(self.gui.info_popover.popup.cget('background'), COLORS['border'])
        self.gui.info_popover.dismiss()
        self.gui.language_name.set('English')
        self.gui._on_language_changed()
        self.assertEqual(self.shell.nav_buttons['experiment'].cget('text'), 'Experiment')
        self.assertEqual(self.gui.language_code, 'en')

    def test_packaged_icons_are_small_and_no_external_graphics_dependency(self):
        assets = Path(__file__).resolve().parents[1] / 'pytracker_gui/assets'
        pngs = [p for p in assets.glob('*.png') if not p.name.startswith('dashboard-')]
        self.assertEqual(len(pngs), 52)
        self.assertLess(sum(p.stat().st_size for p in pngs), 450000)
        self.assertFalse(any('pillow' in line.lower() for line in
                             (Path(__file__).resolve().parents[1] / 'requirements-gui.txt').read_text().splitlines()))


if __name__ == '__main__':
    unittest.main()
