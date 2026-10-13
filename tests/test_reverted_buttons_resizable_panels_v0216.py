"""v0.2.16 contract: v0.2.14 action buttons + only three small icons + native sashes."""
import os
import shutil
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from tkinter import ttk

from pytracker_gui.shell import AppShell
from pytracker_gui.storage import save_settings
from pytracker_gui.theme import COLORS
from tests.test_logs_history_stage1_v0213 import build_run

FIXTURES = Path(__file__).parent / 'fixtures' / 'examples'


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class RevertedButtonsAndPanelsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        home = Path(self.temp.name)
        up = home / 'tobii-pytracker'
        demo = up / 'tobii-pytracker-demo'
        (up / 'src/tobii_pytracker').mkdir(parents=True)
        (up / 'configs').mkdir()
        (up / 'configs/mouse_eyetracker_config.yaml').write_text('mouse: true\n')
        (up / 'configs/eyetracker_config.yaml').write_text('tobii: true\n')
        (up / 'pyproject.toml').write_text('[build-system]\n')
        shutil.copytree(FIXTURES, demo / 'examples')
        (demo / 'tools').mkdir()
        (demo / 'tools/run-demo.sh').write_text('#!/bin/bash\n')
        save_settings(home, {'demo_root':str(demo), 'upstream_root':str(up)})
        build_run(home / 'projects' / 'Example', log='partial')
        self.root = tk.Tk()
        self.root.geometry('1250x900+10+10')
        self.shell = AppShell(self.root, home=home)
        self.root.update()
        self.addCleanup(self.root.destroy)

    def _env_buttons(self):
        env = self.shell.experiment.grid_slaves(row=1, column=0)[0]
        return [env.grid_slaves(row=i, column=3)[0] for i in range(4)]

    def test_original_environment_button_styles_and_only_three_requested_icons(self):
        buttons = self._env_buttons()
        self.assertEqual([b.cget('style') for b in buttons], ['', '', '', ''])
        self.assertFalse(buttons[0].cget('image') == '')  # inherited original save icon
        self.assertFalse(buttons[2].cget('image') == '')  # inherited original folder icon
        # v0.2.20 intentionally restores full-size Detect layout icon;
        # Check Python remains 20 px, with no other changes to buttons.
        for b, size in ((buttons[1], 20), (buttons[3], 40)):
            self.assertTrue(b.cget('image'))
            self.assertEqual((self.root.tk.call('image','width',b.cget('image')),
                              self.root.tk.call('image','height',b.cget('image'))),(size,size))
        self.assertFalse(hasattr(self.shell.experiment,'_setup_action_button_styles'))
        self.assertEqual(COLORS['accent'],ttk.Style().lookup('Accent.TButton','background'))

    def test_original_footer_is_one_row_and_only_apply_has_new_icon(self):
        panes = self.shell.experiment.experiment_panels
        work = self.root.nametowidget(panes.panes()[1])
        footer = work.grid_slaves(row=3,column=0)[0]
        controls = [x for x in footer.winfo_children() if isinstance(x,ttk.Button)]
        labels = [x.cget('text') for x in controls]
        self.assertEqual(len(controls),5)
        self.assertEqual(labels, ['Przywróć oryginał','Eksportuj YAML…','Sprawdź konfigurację',
                                  'Zapisz profil','Zastosuj edycję'])
        apply = controls[-1]
        self.assertTrue(apply.cget('image'))
        self.assertEqual((self.root.tk.call('image','width',apply.cget('image')),
                          self.root.tk.call('image','height',apply.cget('image'))),(20,20))
        self.assertEqual(controls[3].cget('style'),'Accent.TButton')
        self.assertEqual(controls[0].cget('style'),'')
        self.assertEqual(len({c.winfo_manager() for c in controls}),1)
        self.assertEqual(controls[0].winfo_manager(),'pack')

    def test_experiment_sash_is_movable_and_bounded(self):
        panes=self.shell.experiment.experiment_panels
        self.assertEqual(len(panes.panes()),2)
        old=panes.sash_coord(0)[0]
        panes.sash_place(0,old+70,0)
        self.root.update()
        self.assertGreater(panes.sash_coord(0)[0],old+30)
        self.assertGreaterEqual(self.root.nametowidget(panes.panes()[0]).winfo_width(),220)
        self.assertGreaterEqual(self.root.nametowidget(panes.panes()[1]).winfo_width(),650)

    def test_logs_vertical_horizontal_sashes_and_run_history(self):
        self.shell.select_screen('logs'); self.root.update()
        screen=self.shell._screens['logs']
        self.assertEqual(len(screen.logs_panels.panes()),2)
        self.assertEqual(len(screen.project_run_panels.panes()),2)
        x=screen.logs_panels.sash_coord(0)[0]
        screen.logs_panels.sash_place(0,x+65,0); self.root.update()
        self.assertGreater(screen.logs_panels.sash_coord(0)[0],x+30)
        y=screen.project_run_panels.sash_coord(0)[1]
        screen.project_run_panels.sash_place(0,0,y+50); self.root.update()
        self.assertGreater(screen.project_run_panels.sash_coord(0)[1],y+25)
        self.assertEqual(screen.selected_run.run_id,'aB9z0')
        self.assertEqual(screen.report['run_id'],'aB9z0')

    def test_switching_screen_preserves_sashes_and_existing_run(self):
        exp=self.shell.experiment.experiment_panels
        exp.sash_place(0,320,0);self.root.update()
        exp_x=exp.sash_coord(0)[0]
        self.shell.select_screen('logs');self.root.update()
        scr=self.shell._screens['logs'];scr.logs_panels.sash_place(0,305,0);self.root.update()
        logs_x=scr.logs_panels.sash_coord(0)[0]
        self.shell.select_screen('experiment');self.root.update()
        self.assertAlmostEqual(exp.sash_coord(0)[0],exp_x,delta=10)
        self.shell.select_screen('logs');self.root.update()
        self.assertAlmostEqual(scr.logs_panels.sash_coord(0)[0],logs_x,delta=10)
        self.assertEqual(scr.selected_run.run_id,'aB9z0')

    def test_minimum_window_keeps_panels_visible(self):
        self.root.geometry('940x650+10+10');self.root.update()
        ex=self.shell.experiment.experiment_panels
        self.assertGreaterEqual(self.root.nametowidget(ex.panes()[0]).winfo_width(),220)
        self.assertGreaterEqual(self.root.nametowidget(ex.panes()[1]).winfo_width(),650)
        self.shell.select_screen('logs');self.root.update()
        logs=self.shell._screens['logs']
        self.assertGreaterEqual(self.root.nametowidget(logs.logs_panels.panes()[0]).winfo_width(),228)
        self.assertGreaterEqual(self.root.nametowidget(logs.logs_panels.panes()[1]).winfo_width(),390)
        self.assertGreaterEqual(self.root.nametowidget(logs.project_run_panels.panes()[0]).winfo_height(),120)
        self.assertGreaterEqual(self.root.nametowidget(logs.project_run_panels.panes()[1]).winfo_height(),140)

    def test_language_switch_keeps_icons_and_panel_sashes(self):
        exp=self.shell.experiment
        buttons=self._env_buttons()
        images_before=[buttons[1].cget('image'),buttons[3].cget('image')]
        exp.language_name.set('English')
        exp._on_language_changed()
        self.root.update()
        self.assertEqual([buttons[1].cget('image'),buttons[3].cget('image')],images_before)
        self.assertEqual(len(exp.experiment_panels.panes()),2)

if __name__=='__main__': unittest.main()
