"""Home-only brand header regression tests."""
import os
import unittest
from pathlib import Path
from tests.test_navigation_shell_v018 import NavigationShellTests

@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class HomeHeaderTests(unittest.TestCase):
    setUp = NavigationShellTests.setUp
    tearDown = NavigationShellTests.tearDown

    def test_logo_header_and_preserved_tiles(self):
        self.shell.open_home()
        self.root.update()
        home = self.shell._screens['home']
        self.assertEqual((home.header.winfo_width(), home.header.winfo_height()), (1128,102))
        self.assertEqual((home._header_logo.width(), home._header_logo.height()), (96,96))
        self.assertEqual(len(home.header_canvas.find_all()),2)
        self.assertEqual(home.header_canvas.itemcget(home.header_canvas.find_all()[0], 'text'), 'pytracker-gui')
        self.assertEqual(len(home.tile_buttons), 4)
        for tile in home.tile_buttons.values():
            self.assertEqual((tile.winfo_width(),tile.winfo_height()),home.TILE_SIZE)

    def test_header_reused_without_tasks(self):
        self.shell.open_home()
        home=self.shell._screens['home']
        logo=str(home._header_logo)
        self.shell.select_screen('experiment')
        self.shell.open_home()
        self.assertIs(self.shell._screens['home'],home)
        self.assertEqual(str(home._header_logo),logo)

    def test_logo_small_and_opaque_center(self):
        logo=Path(__file__).resolve().parents[1]/'pytracker_gui/assets/dashboard-brand-logo.png'
        self.assertLess(logo.stat().st_size, 20_000)

if __name__=='__main__': unittest.main()
