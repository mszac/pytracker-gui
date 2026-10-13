"""v0.2.19: screenshot-derived initial client size; screen-constrained."""
import os
import unittest
from pytracker_gui.shell import AppShell


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class DefaultWindowSizeTests(unittest.TestCase):
    def test_geometry_uses_screenshot_size_or_screen_available(self):
        import tkinter as tk
        root = tk.Tk()
        try:
            sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
            AppShell(root)
            root.update()
            self.assertEqual(root.winfo_width(), min(1429, max(940, sw - 90)))
            self.assertEqual(root.winfo_height(), min(1097, max(650, sh - 90)))
        finally:
            root.destroy()

if __name__ == '__main__':
    unittest.main()
