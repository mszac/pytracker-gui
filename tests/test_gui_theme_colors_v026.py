"""v0.2.26 scoped UI palette settings: existing theme values only."""
from pathlib import Path
from tempfile import TemporaryDirectory
import os
import tkinter as tk
import unittest

from pytracker_gui import theme
from pytracker_gui.storage import load_settings
from pytracker_gui.shell import AppShell
from pytracker_gui.screens import GuiSettingsScreen


class PaletteContract(unittest.TestCase):
    def tearDown(self):
        theme.configure_saved_palette({})

    def test_factory_blue_and_original_orange(self):
        palette = theme.factory_palette()
        self.assertEqual(palette['ICON_COLOR'], '#22289B')
        self.assertEqual(palette['COLORS']['accent'], '#ff9d45')
        self.assertEqual(palette['COLORS']['selection'], '#ff8931')
        self.assertEqual(palette['COLORS']['accent_hover'], '#ffb775')
        self.assertTrue(theme.valid_hex_color(palette['ICON_COLOR']))
        self.assertFalse(theme.valid_hex_color('#12345g'))
        self.assertFalse(theme.valid_hex_color('#0123'))

    def test_load_accepts_only_existing_keys_and_valid_hex(self):
        defaults = theme.factory_palette()
        theme.configure_saved_palette({'ICON_COLOR': '#123ABC', 'COLORS': {
            'text': '#abcdef', 'unknown_key': '#DDDDDD', 'accent': 'not a color'}})
        self.assertEqual(theme.ICON_COLOR, '#123ABC')
        self.assertEqual(theme.COLORS['text'], '#ABCDEF')
        self.assertEqual(theme.COLORS['accent'], defaults['COLORS']['accent'])
        self.assertEqual(set(theme.COLORS), set(defaults['COLORS']))
        theme.configure_saved_palette({})
        self.assertEqual(theme.ICON_COLOR, '#22289B')
        self.assertEqual(theme.COLORS['text'], defaults['COLORS']['text'])


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'requires Tk display')
class PaletteGuiRuntime(unittest.TestCase):
    def tearDown(self):
        theme.configure_saved_palette({})

    def test_save_validate_relaunch_and_reset_no_new_color_keys(self):
        with TemporaryDirectory() as tmp:
            home = Path(tmp)
            root = tk.Tk()
            try:
                app = AppShell(root, home=home)
                root.update()
                app.select_screen('gui-settings')
                root.update()
                settings = app._screens['gui-settings']
                self.assertEqual(set(settings._color_vars), set(theme.COLORS) | {'ICON_COLOR'})
                self.assertEqual(settings._color_vars['ICON_COLOR'].get(), '#22289B')
                self.assertTrue(settings.colors_card.winfo_exists())
                self.assertGreater(settings.settings_canvas.bbox('all')[3],
                                   settings.settings_canvas.winfo_height())
                self.assertEqual(app.created_screens[-1], 'gui-settings')
                settings._color_vars['ICON_COLOR'].set('#123456')
                settings._color_vars['text'].set('#ABCDEF')
                settings._color_vars['border'].set('red')
                settings._save_colors()
                self.assertIn('border', settings.colors_status.cget('text'))
                self.assertFalse((home / 'settings.json').exists())
                settings._color_vars['border'].set('#334455')
                settings._save_colors()
                stored = load_settings(home)
                self.assertEqual(stored['ICON_COLOR'], '#123456')
                self.assertEqual(stored['COLORS']['text'], '#ABCDEF')
                self.assertEqual(stored['COLORS']['border'], '#334455')
                self.assertEqual(set(stored['COLORS']), set(theme.COLORS))
                # Safe deferred apply: current GUI stays unchanged until restart.
                self.assertEqual(theme.ICON_COLOR, '#22289B')
            finally:
                root.destroy()
            root = tk.Tk()
            try:
                app = AppShell(root, home=home)
                root.update()
                self.assertEqual(theme.ICON_COLOR, '#123456')
                self.assertEqual(theme.COLORS['text'], '#ABCDEF')
                self.assertEqual(theme.COLORS['border'], '#334455')
                selected = theme.icon(root, 'monitor', active=True)
                source = tk.PhotoImage(master=root, file=str(
                    Path(theme.__file__).with_name('assets') / 'monitor-orange.png'))
                self.assertEqual(selected.get(19, 10), source.get(19, 10))
                app.select_screen('gui-settings')
                page = app._screens['gui-settings']
                self.assertEqual(page._color_vars['ICON_COLOR'].get(), '#123456')
                page._reset_colors()
                self.assertEqual(page._color_vars['ICON_COLOR'].get(), '#22289B')
                page._save_colors()
                self.assertEqual(load_settings(home)['ICON_COLOR'], '#22289B')
            finally:
                root.destroy()

    def test_smaller_window_navigation_and_existing_window_setting(self):
        with TemporaryDirectory() as tmp:
            root = tk.Tk()
            try:
                app = AppShell(root, home=Path(tmp))
                root.geometry('940x650')
                root.update()
                app.select_screen('gui-settings')
                root.update()
                page = app._screens['gui-settings']
                page.settings_canvas.yview_moveto(1.0)
                root.update()
                self.assertGreater(page.settings_canvas.yview()[0], 0)
                page.window_size_var.set('1100 × 800')
                page._save()
                self.assertEqual(load_settings(Path(tmp))['window_size'], '1100 × 800')
                app.open_home()
                root.update()
                self.assertEqual(set(app._screens['home'].tile_buttons),
                                 {'experiment', 'logs', 'statistics', 'manual'})
                app.select_screen('manual')
                root.update()
                self.assertEqual(len(app._screens['manual'].tabs.tabs()), 4)
            finally:
                root.destroy()


if __name__ == '__main__':
    unittest.main()
