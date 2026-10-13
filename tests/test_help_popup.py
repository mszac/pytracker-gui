"""Real Tk rendering and click tests; run with a working display (Xvfb on Linux)."""
import os
import tkinter as tk
import unittest
from tkinter import ttk
from pytracker_gui.help_widgets import BLUE, InfoButton, InfoPopover
from pytracker_gui.parameter_help import get_parameter_help


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name=='nt', 'Display is required')
class HelpPopupTests(unittest.TestCase):
    def setUp(self):
        self.root=tk.Tk()
        self.pop=InfoPopover(self.root,get_parameter_help)
        self.frame=ttk.Frame(self.root)
        self.frame.pack()
        self.icon=InfoButton(self.frame,help_key='display.monitor.width',callback=self.pop.toggle)
        self.icon.pack()
        self.root.update()

    def tearDown(self):
        self.pop.dismiss()
        self.root.destroy()

    def test_blue_info_icon_shows_short_text_on_click(self):
        self.assertEqual(self.icon.itemcget(self.icon.find_all()[0],'fill'),BLUE)
        self.assertEqual(self.icon.itemcget(self.icon.find_all()[1],'text'),'i')
        self.icon.invoke()
        self.assertIsNotNone(self.pop.popup)
        self.assertTrue(self.pop.popup.winfo_exists())
        self.assertEqual(self.pop.active,'display.monitor.width')
        self.assertIn(get_parameter_help('display.monitor.width')['short'],
                      ' '.join(w.cget('text') for w in self._labels(self.pop.popup)))
        self.icon.invoke()  # clicking the same 'i' toggles the bubble off
        self.assertIsNone(self.pop.popup)

    def _labels(self,w):
        out=[]
        for child in w.winfo_children():
            if isinstance(child,tk.Label):out.append(child)
            out.extend(self._labels(child))
        return out

    def test_one_popup_at_a_time_and_close(self):
        other=InfoButton(self.frame,help_key='runtime.log_level',callback=self.pop.toggle)
        other.pack()
        self.icon.invoke()
        first=self.pop.popup
        other.invoke()
        self.assertIsNotNone(self.pop.popup)
        self.assertNotEqual(first,self.pop.popup)
        self.assertEqual(self.pop.active,'runtime.log_level')
        self.pop.dismiss()
        self.assertIsNone(self.pop.popup)


if __name__=='__main__':unittest.main()
