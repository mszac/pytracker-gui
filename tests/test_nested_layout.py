"""No network, Python 3.10 compatible: nested checkout discovery & read-only gates."""
import tempfile
import unittest
from pathlib import Path
from pytracker_gui.catalog import CATALOG
from pytracker_gui.layout import (canonical_roots, choose_roots, default_eye_config,
                                  format_layout_report, validate_layout)


class NestedLayoutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name) / 'tobii-pytracker'
        self.gui = self.parent / 'pytracker-gui'
        self.gui.mkdir(parents=True)
        self.demo = self.parent / 'tobii-pytracker-demo'
        (self.parent / 'src/tobii_pytracker').mkdir(parents=True)
        (self.parent / 'configs').mkdir(parents=True)
        (self.parent / 'pyproject.toml').write_text('')
        (self.parent / 'configs/mouse_eyetracker_config.yaml').write_text('')
        (self.parent / 'configs/eyetracker_config.yaml').write_text('')
        (self.demo / 'tools').mkdir(parents=True)
        (self.demo / 'tools/run-demo.sh').write_text('#!/bin/sh\n')
        for d in CATALOG:
            for block in d.blocks:
                p = self.demo / block.config_relpath
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('dataset: {}\n')

    def test_default_from_gui_location_not_cwd(self):
        self.assertEqual(canonical_roots(self.gui), (self.parent, self.demo))
        self.assertEqual(choose_roots({},gui_root=self.gui),(self.parent,self.demo))
        self.assertEqual(validate_layout(self.parent,self.demo),[])
        self.assertTrue(format_layout_report(self.gui)[1])

    def test_stale_old_settings_do_not_beat_neighbor_checkouts(self):
        upstream,demo=choose_roots({'upstream_root':'/not/here','demo_root':'/not/here'},gui_root=self.gui)
        self.assertEqual((upstream,demo),(self.parent,self.demo))

    def test_incorrect_sibling_layout_fails_closed(self):
        wrong=self.parent.parent/'tobii-pytracker-demo'
        wrong.mkdir()
        errs=validate_layout(self.parent,wrong)
        self.assertTrue(any('musi być' in e for e in errs))
        (self.demo/'examples/test_demo/config.native.yaml').unlink()
        self.assertTrue(any('test_demo/config.native.yaml' in e for e in validate_layout(self.parent,self.demo)))

    def test_default_iohub_for_mouse_no_gaze_tobii(self):
        self.assertEqual(default_eye_config(self.parent,'mouse'),self.parent/'configs/mouse_eyetracker_config.yaml')
        self.assertEqual(default_eye_config(self.parent,'none'),self.parent/'configs/mouse_eyetracker_config.yaml')
        self.assertEqual(default_eye_config(self.parent,'tobii'),self.parent/'configs/eyetracker_config.yaml')


if __name__ == '__main__':unittest.main()
