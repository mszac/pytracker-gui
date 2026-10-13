"""v0.2.27: only Experiment idle icons and heading presentation differ."""
import os
import tempfile
import tkinter as tk
import unittest
from pathlib import Path

from pytracker_gui import theme
from pytracker_gui.shell import AppShell
from pytracker_gui.storage import save_settings
from pytracker_gui.app import EXPERIMENT_DEFAULT_ICON_COLOR


class ExperimentPresentationContract(unittest.TestCase):
    def test_scoped_color_constant_and_unchanged_global_factory(self):
        self.assertEqual(EXPERIMENT_DEFAULT_ICON_COLOR, '#A46628')
        self.assertEqual(theme.factory_palette()['ICON_COLOR'], '#22289B')
        self.assertEqual(theme.factory_palette()['COLORS']['accent'], '#ff9d45')


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'requires Tk display')
class ExperimentPresentationRuntime(unittest.TestCase):
    def test_static_heading_and_idle_scoped_color(self):
        with tempfile.TemporaryDirectory() as temp:
            root = tk.Tk()
            try:
                shell = AppShell(root, home=Path(temp))
                root.update()
                experiment = shell.experiment
                self.assertEqual(experiment.demo_label.cget('text'), 'Experiment setup')
                self.assertEqual(experiment.demo_label.cget('style'), 'Heading.TLabel')
                self.assertIs(experiment._experiment_icon('monitor'),
                              theme.icon(root, 'monitor', color='#A46628'))
                self.assertIsNot(experiment._experiment_icon('monitor'), theme.icon(root, 'monitor'))
                self.assertIs(experiment._experiment_icon('monitor', True), theme.icon(root, 'monitor', True))
                experiment.tabs.select(experiment.pages['Monitor'])
                root.update()
                self.assertEqual(str(experiment.tabs.tab(experiment.pages['Monitor'], 'image')[0]),
                                 str(theme.icon(root, 'monitor', True)))
                self.assertEqual(str(experiment.tabs.tab(experiment.pages['Dane'], 'image')[0]),
                                 str(theme.icon(root, 'data', color='#A46628')))
                self.assertEqual(str(shell.nav_buttons['logs'].cget('image')[0]),
                                 str(theme.icon(root, 'logs')))
                if len(experiment.listbox.get(0, 'end')) > 1:
                    experiment._select_demo(1, ask=False)
                    root.update()
                    self.assertEqual(experiment.demo_label.cget('text'), 'Experiment setup')
                experiment._apply_language()
                self.assertEqual(experiment.demo_label.cget('text'), 'Experiment setup')
            finally:
                root.destroy()

    def test_explicit_saved_icon_preference_takes_precedence(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            save_settings(home, {'ICON_COLOR': '#123456'})
            root = tk.Tk()
            try:
                shell = AppShell(root, home=home)
                root.update()
                experiment = shell.experiment
                self.assertIs(experiment._experiment_icon('monitor'),
                              theme.icon(root, 'monitor', color='#123456'))
                self.assertIs(experiment._experiment_icon('monitor', True),
                              theme.icon(root, 'monitor', True))
            finally:
                root.destroy()
                theme.configure_saved_palette({})


if __name__ == '__main__':
    unittest.main()
