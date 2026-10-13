"""v0.2.18: bounded static image-only dashboard, four original routes."""
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.screens import DashboardScreen
from tests.test_navigation_shell_v018 import NavigationShellTests


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class FixedImageDashboardTests(unittest.TestCase):
    setUp = NavigationShellTests.setUp
    tearDown = NavigationShellTests.tearDown

    def open_dashboard(self):
        self.shell.open_home()
        self.root.update()
        return self.shell._screens['home']

    def test_lazily_created_at_brand_click(self):
        self.assertNotIn('home', self.shell.created_screens)
        home = self.open_dashboard()
        self.assertIsInstance(home, DashboardScreen)
        self.assertEqual(tuple(home.tile_buttons), ('experiment', 'logs', 'statistics', 'manual'))
        self.assertEqual(len(home._tile_images), 4)
        self.shell.select_screen('experiment')
        self.assertIs(self.open_dashboard(), home)

    def test_exact_png_dimensions_fixed_before_and_after_resizing(self):
        home = self.open_dashboard()
        width, height = home.TILE_SIZE
        for key, tile in home.tile_buttons.items():
            self.assertEqual((tile.winfo_width(), tile.winfo_height()), (width, height))
            self.assertEqual((home._tile_images[key].width(), home._tile_images[key].height()), (width, height))
            self.assertIn(str(home._tile_images[key]), str(tile.cget('image')))
        original = self.root.geometry()
        try:
            self.root.geometry('940x650')
            self.root.update()
            self.assertEqual(home.hscroll.winfo_manager(), 'pack')
            self.assertEqual(home.vscroll.winfo_manager(), 'pack')
            self.root.geometry('1500x1000')
            self.root.update()
            self.assertFalse(home.hscroll.winfo_manager())
            self.assertFalse(home.vscroll.winfo_manager())
            for key, tile in home.tile_buttons.items():
                self.assertEqual((tile.winfo_width(), tile.winfo_height()), (width, height), key)
        finally:
            self.root.geometry(original)
            self.root.update()

    def test_bundled_images_small_and_all_four_present(self):
        assets = Path(__file__).resolve().parents[1] / 'pytracker_gui' / 'assets'
        for key, _, _ in DashboardScreen.TILES:
            png = assets / f'dashboard-{key}.png'
            self.assertTrue(png.is_file())
            self.assertLess(png.stat().st_size, 350_000)

    def test_four_tiles_still_route_without_yaml_commit_or_runner_start(self):
        with (patch.object(self.gui, '_commit_tab', side_effect=AssertionError('GUI YAML commit')),
              patch.object(self.gui.runner, 'start', side_effect=AssertionError('Started experiment'))):
            for key, _, _ in DashboardScreen.TILES:
                home = self.open_dashboard()
                home.tile_buttons[key].invoke()
                self.assertEqual(self.shell.current_screen, key)

    def test_language_metadata_changes_not_image_bytes(self):
        home = self.open_dashboard()
        image_ids = {key: str(t.cget('image')) for key,t in home.tile_buttons.items()}
        self.gui.language_name.set('English')
        self.gui._on_language_changed()
        self.assertEqual(home.tile_buttons['experiment'].cget('text'), 'Experiment')
        self.assertEqual(image_ids, {key: str(t.cget('image')) for key,t in home.tile_buttons.items()})
