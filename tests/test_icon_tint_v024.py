"""v0.2.24: icon-only tint parameter without touching the global orange theme."""
import base64
import json
import os
import tempfile
import tkinter as tk
import unittest
import zlib
from pathlib import Path
from unittest.mock import patch

from pytracker_gui import theme
from pytracker_gui.shell import AppShell

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'pytracker_gui' / 'assets'


class IconTintAssetTests(unittest.TestCase):
    def test_named_burgundy_hex_parameter_is_independent(self):
        # v0.2.25 supersedes v0.2.24 default tint, not the independent parameter.
        self.assertEqual(theme.ICON_COLOR, '#22289B')  # v0.2.26 supersedes former burgundy default
        self.assertNotEqual(theme.ICON_COLOR.lower(), theme.COLORS['accent'].lower())
        self.assertEqual(theme.COLORS['accent'], '#ff9d45')
        self.assertEqual(theme.COLORS['selection'], '#ff8931')

    def test_alpha_masks_are_lossless_small_and_cover_all_small_icons(self):
        path = ASSETS / 'icon-alpha-masks.json'
        masks = json.loads(path.read_text(encoding='utf-8'))
        self.assertLess(path.stat().st_size, 20000)
        expected = {p.name[:-len('-muted.png')] for p in ASSETS.glob('*-muted.png')}
        self.assertEqual(set(masks), expected)
        for name, m in masks.items():
            with self.subTest(name=name):
                self.assertEqual((m['w'], m['h']), (40, 40))
                self.assertEqual(len(zlib.decompress(base64.b64decode(m['alpha']))), 1600)
        self.assertNotIn('brand-logo', masks)
        self.assertFalse(any(key.startswith('dashboard-') for key in masks))

    def test_theme_depends_only_on_python_standard_library_and_tk(self):
        self.assertNotIn('PIL', (ROOT / 'pytracker_gui' / 'theme.py').read_text(encoding='utf-8'))
        self.assertFalse(any('pillow' in s.lower() for s in
                             (ROOT / 'requirements-gui.txt').read_text(encoding='utf-8').splitlines()))


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class IconTintRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_tint_preserves_alpha_and_supports_another_hex_color(self):
        first = theme.icon(self.root, 'monitor')
        selected = theme.icon(self.root, 'monitor', True)
        self.assertEqual((first.width(), first.height()), (40, 40))
        self.assertIs(first, theme.icon(self.root, 'monitor'))
        self.assertIsNot(first, selected)  # existing selection image identities
        expected = tuple(bytes.fromhex(theme.ICON_COLOR[1:]))
        mask = zlib.decompress(base64.b64decode(theme._icon_masks()['monitor']['alpha']))
        opaque_pos = next(i for i, a in enumerate(mask) if a == 255)
        x, y = opaque_pos % 40, opaque_pos // 40
        self.assertEqual(first.get(x, y), expected)
        source = tk.PhotoImage(master=self.root, file=str(ASSETS / 'monitor-orange.png'))
        self.assertEqual(selected.get(x, y), source.get(x, y))
        self.assertIs(selected, theme.icon(self.root, 'monitor', True))
        with patch.object(theme, 'ICON_COLOR', '#A9CBD2'):
            other = theme.icon(self.root, 'monitor')
            self.assertIsNot(other, first)
            self.assertEqual(other.get(x, y), (169, 203, 210))
            self.assertIs(theme.icon(self.root, 'monitor'), other)
        self.assertIs(theme.icon(self.root, 'monitor'), first)

    def test_ink_buttons_logo_and_orange_style_remain_unmodified(self):
        theme.apply_theme(self.root)
        ink = theme.icon(self.root, 'check', active='ink')
        opaque = [ink.get(x,y) for y in range(40) for x in range(40)
                  if not bool(ink.transparency_get(x,y))]
        self.assertTrue(any(sum(pixel) < 350 for pixel in opaque))
        self.assertNotEqual(ink.get(19, 10), tuple(bytes.fromhex(theme.ICON_COLOR[1:])))
        self.assertIs(ink, theme.icon(self.root, 'check', active='ink'))
        brand = theme.brand_logo(self.root)
        self.assertIs(brand, theme.brand_logo(self.root))
        from tkinter import ttk
        style = ttk.Style(self.root)
        self.assertEqual(style.lookup('Accent.TButton', 'background'), theme.COLORS['accent'])
        self.assertEqual(style.lookup('Toolbutton', 'foreground', ['selected']), theme.COLORS['accent'])

    def test_navigation_tabs_and_compact_buttons_share_tint_without_new_actions(self):
        with tempfile.TemporaryDirectory() as temporary:
            shell = AppShell(self.root, home=Path(temporary))
            self.root.update()
            before = shell.experiment.runner
            for page in ('logs', 'manual', 'gui-settings', 'statistics', 'experiment'):
                shell.select_screen(page)
                self.root.update()
                self.assertIs(shell.experiment.runner, before)
            self.assertEqual(shell.current_screen, 'experiment')
            self.assertEqual(shell.experiment.tabs.tab(shell.experiment.pages['Monitor'], 'image') != '', True)
            self.assertIn('gui-settings', shell.created_screens)
            self.assertEqual(shell.current_screen, 'experiment')


if __name__ == '__main__':
    unittest.main()
