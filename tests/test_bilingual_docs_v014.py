"""Coverage, documentation parity, stable status boundaries for v0.1.4."""
import json
import unittest
from pathlib import Path

from pytracker_gui.parameter_help import parameter_catalog, english_tooltip_catalog, get_parameter_help
from tools.render_parameter_manual import render, render_en, GROUP_EN, STATUS_EN, STATUS_PL
from pytracker_gui.catalog import CATALOG

ROOT=Path(__file__).resolve().parents[1]

class BilingualDocsV014Tests(unittest.TestCase):
    def test_all_87_entries_have_two_complete_languages(self):
        pl=parameter_catalog()
        en=english_tooltip_catalog()
        self.assertEqual(len(pl),87)
        self.assertEqual(set(pl),set(en))
        for key in pl:
            local_pl=get_parameter_help(key,'pl')
            local_en=get_parameter_help(key,'en')
            self.assertEqual(local_en['key'],key)
            self.assertEqual(local_en['source'],local_pl['source'])
            self.assertEqual(local_en['status'],local_pl['status'])
            self.assertEqual(local_en['group'],local_pl['group'])
            for rec in (local_pl,local_en):
                self.assertTrue(rec['title'].strip(),key)
                self.assertGreaterEqual(len(rec['short']),25,key)
                self.assertLessEqual(len(rec['short']),125,key)
                self.assertEqual(rec['short'][-1],'.',key)
                self.assertNotIn('\n',rec['short'],key)
                self.assertGreaterEqual(len(rec['long'].split('. ')),3,key)
                self.assertGreaterEqual(len(rec['long']),120,key)
                self.assertTrue(rec['long'].endswith('.'),key)
        self.assertEqual(set(STATUS_PL),set(STATUS_EN))

    def test_manual_parity_and_deterministic_output(self):
        p_pl=ROOT/'docs/PARAMETER_MANUAL_PL.md'
        p_en=ROOT/'docs/PARAMETER_MANUAL_EN.md'
        self.assertEqual(p_pl.read_text(encoding='utf8'),render('pl'))
        self.assertEqual(p_en.read_text(encoding='utf8'),render('en'))
        self.assertEqual(render(),render('pl'))
        self.assertEqual(render_en(),render('en'))
        keys=list(parameter_catalog())
        for lang in ('pl','en'):
            text=render(lang)
            self.assertEqual(text.count('\n### `'),87)
            for key in keys:
                self.assertEqual(text.count('### `'+key+'`'),1,key)
            for label in STATUS_PL:
                self.assertIn('`'+label+'`',text)
        self.assertEqual(set(GROUP_EN),{x['group'] for x in parameter_catalog().values()})

    def test_user_guides_cover_same_demo_inventory_and_scope(self):
        pl=(ROOT/'docs/USER_GUIDE_PL.md').read_text(encoding='utf8')
        en=(ROOT/'docs/USER_GUIDE_EN.md').read_text(encoding='utf8')
        self.assertEqual(len(CATALOG),7)
        for key in ('Test Demo','UX A/B Text','Time-Series Noise','Text Search','Image Semantic',
                    'Machine Vibration','PV Power','NO_GAZE','MOUSEGAZE','TOBII','87','YAML','ioHub',
                    'PARAMETER_MANUAL_PL.md','PARAMETER_MANUAL_EN.md'):
            self.assertIn(key,pl)
            self.assertIn(key,en)
        for status in STATUS_PL:
            self.assertIn('`'+status+'`',pl)
            self.assertIn('`'+status+'`',en)
        self.assertIn('nie uruchamia',pl.lower())
        self.assertIn('not yet an experiment launcher',en.lower())

    def test_install_guides_and_indexes_have_language_pairs(self):
        for prefix in ('README_WINDOWS_GIT_BASH_',):
            for lang in ('PL','EN'):
                text=(ROOT/(prefix+lang+'.md')).read_text(encoding='utf8')
                for key in ('git clone https://github.com/sbobek/tobii-pytracker.git',
                            'git clone https://github.com/mszac/tobii-pytracker-demo.git',
                            'pytracker-env','--check-layout','run_gui.py','PARAMETER_MANUAL_PL.md',
                            'PARAMETER_MANUAL_EN.md','v0.1.4'):
                    self.assertIn(key,text)
        for lang in ('PL','EN'):
            text=(ROOT/'docs'/('DOCUMENTATION_INDEX_'+lang+'.md')).read_text(encoding='utf8')
            for fname in ('USER_GUIDE_PL.md','USER_GUIDE_EN.md','PARAMETER_MANUAL_PL.md',
                          'PARAMETER_MANUAL_EN.md','README_WINDOWS_GIT_BASH_PL.md',
                          'README_WINDOWS_GIT_BASH_EN.md'):
                self.assertIn(fname,text)

    def test_gui_behavior_modules_frozen_from_parent_release(self):
        """Documentation test checks documented integration boundaries, not source snapshots."""
        gui_py=(ROOT/'pytracker_gui/app.py').read_text(encoding='utf8')
        self.assertIn('from .runner import ExperimentRunner',gui_py)
        self.assertIn("'gui_launch_uses_current_yaml_snapshot_and_selected_runtime_flags':True",gui_py)
        self.assertIn('self.help_lookup(help_key)', (ROOT/'pytracker_gui/help_widgets.py').read_text(encoding='utf8'))
        self.assertIn('PARAMETER_MANUAL_EN.md',gui_py)
        self.assertNotIn('webbrowser.open',gui_py)

if __name__=='__main__':
    unittest.main()
