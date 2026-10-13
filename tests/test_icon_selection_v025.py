"""v0.2.25 selected orange icons and darker configurable idle burgundy."""
import os
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch
from tkinter import ttk

from pytracker_gui import theme
from pytracker_gui.shell import AppShell


class StaticIconContract(unittest.TestCase):
    def test_darker_burgundy_and_preserved_orange(self):
        self.assertEqual(theme.ICON_COLOR, '#22289B')  # v0.2.26 supersedes former burgundy default
        self.assertEqual(theme.COLORS['accent'], '#ff9d45')
        self.assertEqual(theme.COLORS['selection'], '#ff8931')
        self.assertEqual(theme.COLORS['accent_hover'], '#ffb775')


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class IconStateRuntime(unittest.TestCase):
    @staticmethod
    def image_id(value):
        return value[0] if isinstance(value, tuple) else str(value)

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_idle_tint_selected_png_ink_png_and_cache(self):
        name = 'monitor'
        idle = theme.icon(self.root, name)
        selected = theme.icon(self.root, name, active=True)
        orange_source = tk.PhotoImage(master=self.root, file=str(Path(theme.__file__).with_name('assets') / 'monitor-orange.png'))
        self.assertEqual((idle.width(), idle.height()), (40, 40))
        self.assertEqual((selected.width(), selected.height()), (40, 40))
        self.assertIs(theme.icon(self.root, name), idle)
        self.assertIs(theme.icon(self.root, name, True), selected)
        self.assertIsNot(idle, selected)
        points = [(x,y) for y in range(40) for x in range(40) if not orange_source.transparency_get(x,y)]
        self.assertGreater(len(points), 20)
        for xy in points[::max(1,len(points)//25)]:
            self.assertEqual(selected.get(*xy), orange_source.get(*xy))
        with patch.object(theme,'ICON_COLOR','#789ABC'):
            changed = theme.icon(self.root,name)
            self.assertIsNot(changed,idle)
            self.assertIs(theme.icon(self.root,name,True),selected)
        self.assertIs(theme.icon(self.root,name),idle)
        ink = theme.icon(self.root,'check','ink')
        self.assertIs(theme.icon(self.root,'check','ink'),ink)

    def test_nav_and_notebook_selected_icons_follow_orange_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            shell = AppShell(self.root,home=Path(tmp))
            self.root.update()
            self.assertEqual(self.image_id(shell.nav_buttons['experiment'].cget('image')),str(theme.icon(self.root,'experiment',True)))
            shell.select_screen('logs')
            self.root.update()
            self.assertEqual(self.image_id(shell.nav_buttons['logs'].cget('image')),str(theme.icon(self.root,'logs',True)))
            self.assertEqual(self.image_id(shell.nav_buttons['experiment'].cget('image')),str(theme.icon(self.root,'experiment')))
            self.assertEqual(self.image_id(shell.experiment.tabs.tab(shell.experiment.pages['Dane'],'image')),str(theme.icon(self.root,'data',True)))
            # Tab changing must swap selected and idle icons, without affecting functions.
            shell.select_screen('experiment')
            shell.experiment.tabs.select(shell.experiment.pages['Monitor'])
            self.root.update()
            self.assertEqual(self.image_id(shell.experiment.tabs.tab(shell.experiment.pages['Monitor'],'image')),str(theme.icon(self.root,'monitor',True)))
            self.assertEqual(self.image_id(shell.experiment.tabs.tab(shell.experiment.pages['Dane'],'image')),str(theme.icon(self.root,'data', color='#A46628')))
            style=ttk.Style(self.root)
            self.assertEqual(style.lookup('Toolbutton','foreground',['selected']),theme.COLORS['accent'])
            self.assertEqual(style.lookup('TNotebook.Tab','foreground',['selected']),theme.COLORS['accent'])


if __name__=='__main__':
    unittest.main()
