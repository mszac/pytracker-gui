"""Requires a graphical display; CI can run under xvfb-run on Linux."""
import os
import shutil
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from pytracker_gui.app import PytrackerGUI, TABS
from pytracker_gui.storage import save_settings
from pytracker_gui.yamlconfig import get_value

ROOT=Path(__file__).parent/'fixtures'

@unittest.skipUnless(os.environ.get('DISPLAY') or os.name=='nt', 'Display is required')
class GuiSmoke(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.home=Path(self.tmp.name)
        self.upstream = self.home/'tobii-pytracker'
        self.demo_root = self.upstream/'tobii-pytracker-demo'
        (self.upstream/'src/tobii_pytracker').mkdir(parents=True)
        (self.upstream/'configs').mkdir(parents=True)
        (self.upstream/'configs/mouse_eyetracker_config.yaml').write_text('mouse: true\n')
        (self.upstream/'configs/eyetracker_config.yaml').write_text('tobii: true\n')
        (self.upstream/'pyproject.toml').write_text('[build-system]\n')
        shutil.copytree(ROOT/'examples', self.demo_root/'examples')
        (self.demo_root/'tools').mkdir()
        (self.demo_root/'tools/run-demo.sh').write_text('#!/bin/bash\n')
        save_settings(self.home,{'demo_root':str(self.demo_root),'upstream_root':str(self.upstream)})
        self.root=tk.Tk()
        self.root.withdraw()
        self.gui=PytrackerGUI(self.root,home=self.home)
        self.root.update()

    def tearDown(self):
        self.root.destroy()
        self.tmp.cleanup()

    def test_every_variant_and_switch_blocks_without_cross_writing(self):
        from pytracker_gui.catalog import CATALOG
        for i,d in enumerate(CATALOG):
            self.gui._select_demo(i,ask=False)
            self.root.update()
            self.assertTrue(self.gui.loaded,d.key)
            self.assertEqual(self.gui.demo.key,d.key)
        self.gui._select_demo(3,ask=False)
        self.root.update()
        self.assertEqual(self.gui.active_block_key,'machine')
        self.gui.active_tab='Dane'
        self.gui.field_vars['Dane']['output.folder'][1].set('custom/machine')
        self.gui.block_combo.current(1)
        self.gui._change_block()
        self.assertEqual(get_value(self.gui.docs['machine'],'output.folder'),'custom/machine')
        self.assertEqual(get_value(self.gui.docs['pv'],'output.folder'),'output/timeseries_noise_demo/pv')
        self.assertEqual(self.gui.active_block_key,'pv')
        self.assertTrue(self.gui._save())
        self.assertTrue((self.home/'projects/ts_machine_pv/profiles/ts_machine_pv/machine.yaml').is_file())
        self.assertTrue((self.home/'projects/ts_machine_pv/profiles/ts_machine_pv/pv.yaml').is_file())

    def test_info_buttons_for_monitor_yaml_and_runtime(self):
        from pytracker_gui.help_widgets import InfoButton
        def icons(widget):
            out = []
            for child in widget.winfo_children():
                if isinstance(child, InfoButton):
                    out.append(child)
                out.extend(icons(child))
            return out
        monitor_icons = icons(self.gui.pages['Monitor'])
        self.assertEqual(len(monitor_icons), 5)
        for key in ('display.monitor.width', 'display.monitor.resolution'):
            button = next(icon for icon in monitor_icons if icon.help_key == key)
            button.invoke()
            self.assertEqual(self.gui.info_popover.active,key)
            self.assertTrue(self.gui.info_popover.popup.winfo_exists())
        self.gui.tabs.select(self.gui.pages['YAML'])
        self.root.update()
        self.assertIsNone(self.gui.info_popover.popup)
        self.assertIn('gui.yaml_editor', [i.help_key for i in icons(self.gui.pages['YAML'])])
        self.assertEqual({'runtime.loop_count','runtime.log_level','runtime.enable_voice','runtime.raw_data'},
                         {i.help_key for i in icons(self.gui.pages['Uruchomienie'])})
        self.assertEqual(2, len(icons(self.gui.pages['Instrukcje'])))

    def test_form_and_yaml_roundtrip_through_gui(self):
        self.assertTrue(self.gui.loaded)
        self.gui.tabs.select(self.gui.pages['Monitor'])
        self.root.update()
        self.gui.field_vars['Monitor']['display.monitor.width'][1].set('44.5')
        self.assertTrue(self.gui._commit_tab())
        self.assertEqual(get_value(self.gui.docs['main'],'display.monitor.width'),44.5)
        self.gui.tabs.select(self.gui.pages['YAML'])
        self.root.update()
        self.gui.yaml_editor.insert('end','\nnew_ui_note: preserved\n')
        self.gui.raw_dirty=True
        self.assertTrue(self.gui._commit_tab())
        self.assertEqual(self.gui.docs['main']['new_ui_note'],'preserved')
        self.assertTrue(self.gui._save())
        original=(self.demo_root/'examples/test_demo/config.native.yaml').read_text(encoding='utf-8')
        self.assertNotIn('new_ui_note',original)

if __name__=='__main__':unittest.main()
