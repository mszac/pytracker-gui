"""v0.2.20: enlarge only Environment Save paths and Detect layout icon artwork."""
import os
from pathlib import Path
import tkinter as tk
import unittest
from pytracker_gui.app import PytrackerGUI
from pytracker_gui.theme import icon


@unittest.skipUnless(os.name == 'nt' or os.environ.get('DISPLAY'), 'Tk required')
class EnvironmentIconsV0220(unittest.TestCase):
    def test_two_target_icons_and_unchanged_other_icons(self):
        root = tk.Tk()
        try:
            app = PytrackerGUI(root)
            root.update()
            env = app.grid_slaves(row=1, column=0)[0]
            buttons = [env.grid_slaves(row=i, column=3)[0] for i in range(4)]
            dims = [(root.tk.call('image','width',b.cget('image')),
                     root.tk.call('image','height',b.cget('image'))) for b in buttons]
            self.assertEqual(dims, [(40,40),(20,20),(40,40),(40,40)])
            self.assertEqual(buttons[2].cget('image'), buttons[3].cget('image'))
            self.assertNotEqual(buttons[0].cget('image'),icon(root,'save').__str__())
            self.assertEqual([b.cget('style') for b in buttons], ['', '', '', ''])
            self.assertEqual([b.grid_info()['sticky'] for b in buttons], ['ew']*4)
            app.language_name.set('English'); app._on_language_changed(); root.update()
            self.assertEqual([(root.tk.call('image','width',b.cget('image')),
                              root.tk.call('image','height',b.cget('image'))) for b in buttons],dims)
        finally:
            root.destroy()

    def test_save_graphic_asset_only_is_distinct(self):
        assets=Path(__file__).resolve().parents[1]/'pytracker_gui/assets'
        original=(assets/'save-muted.png').read_bytes()
        new=(assets/'save-environment-muted.png').read_bytes()
        self.assertNotEqual(original,new)


if __name__=='__main__':unittest.main()
