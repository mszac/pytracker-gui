"""v0.2.5: starter-project terminology and EN-only selectable-option reference."""
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.catalog import CATALOG
from pytracker_gui.fields import DATASET_FIELDS
from pytracker_gui.i18n import translate
from pytracker_gui.parameter_help import parameter_catalog, get_parameter_help
from tools.render_parameter_manual import render

ROOT = Path(__file__).resolve().parents[1]


class ProjectNamingManualOptionsTests(unittest.TestCase):
    def test_polish_canonical_catalog_and_manual_unchanged(self):
        self.assertEqual(len(parameter_catalog()), 87)
        self.assertEqual((ROOT/'docs/PARAMETER_MANUAL_PL.md').read_text(encoding='utf-8'), render('pl'))
        self.assertNotIn('**Available options:**',render('pl'))
        self.assertNotIn('options', get_parameter_help('gui.gaze', 'pl'))

    def test_english_documented_discrete_choices_complete(self):
        records = [get_parameter_help(key, 'en') for key in parameter_catalog()]
        choices = [r for r in records if r.get('options')]
        self.assertGreaterEqual(len(choices), 25)
        self.assertEqual(len(choices), 28)
        for record in choices:
            values = [item['value'] for item in record['options']]
            self.assertEqual(len(values),len(set(values)),record['key'])
            for item in record['options']:
                self.assertTrue(item['value'].strip(),record['key'])
                self.assertGreaterEqual(len(item['description']), 45,record['key'])
                self.assertTrue(item['description'].endswith('.'),record['key'])
        for field in DATASET_FIELDS:
            if field.kind == 'choice':
                documented = {i['value'] for i in get_parameter_help(field.path,'en')['options']}
                self.assertEqual(documented,set(field.options),field.path)
        documented = {i['value'] for i in get_parameter_help('gui.variant','en')['options']}
        self.assertEqual(documented,{demo.key for demo in CATALOG})
        self.assertEqual({i['value'] for i in get_parameter_help('gui.gaze','en')['options']},
                         {'NO_GAZE','MOUSEGAZE','TOBII'})
        self.assertIn('**Available options:**',render('en'))
        self.assertEqual(render('en'),(ROOT/'docs/PARAMETER_MANUAL_EN.md').read_text(encoding='utf-8'))

    def test_project_ui_translations_not_runtime_identifiers(self):
        cases = {
            'Projekty startowe (7)': 'Starter projects (7)',
            'Wybierz projekt startowy': 'Select a starter project',
            'Uruchom projekt': 'Launch project',
            'Zatrzymaj projekt': 'Stop project',
            'Katalog projektów startowych': 'Starter-project repository',
        }
        for pl,en in cases.items():
            self.assertEqual(translate(pl, 'en'), en)
            self.assertEqual(translate(pl, 'pl'), pl)
        # Keys used by historical manifests and project profiles remain stable.
        self.assertEqual(CATALOG[0].key, 'test_en')
        self.assertEqual(CATALOG[-1].key,'image_en')


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt','Tk display required')
class ManualOptionsTkTests(unittest.TestCase):
    def setUp(self):
        from tests.test_navigation_shell_v018 import NavigationShellTests
        NavigationShellTests.setUp(self)
    def tearDown(self):
        from tests.test_navigation_shell_v018 import NavigationShellTests
        NavigationShellTests.tearDown(self)

    def test_english_manual_options_and_polish_unmodified(self):
        self.shell.open_manual('gui.gaze')
        man = self.shell._screens['manual']
        man.set_language('en','en')
        text = man.details.get('1.0','end')
        self.assertIn('Available options', text)
        self.assertIn('MOUSEGAZE', text)
        self.assertIn('TOBII', text)
        man.search_var.set('MOUSEGAZE')
        self.assertIn('gui.gaze', man.visible_keys)
        man.set_language('pl','pl')
        man.show_parameter('gui.gaze')
        self.assertNotIn('Available options', man.details.get('1.0','end'))

    def test_project_labels_and_navigation_no_runtime_changes(self):
        from tkinter import ttk
        def descendants(widget):
            for child in widget.winfo_children():
                yield child
                yield from descendants(child)
        headers = [w.cget('text') for w in descendants(self.gui) if isinstance(w, ttk.LabelFrame)]
        self.assertIn('Projekty startowe (7)', headers)
        with patch.object(self.gui.runner,'start',side_effect=AssertionError('Do not launch')), \
             patch.object(self.gui.runner,'stop',side_effect=AssertionError('Do not stop')):
            self.shell.select_screen('manual')
            self.shell.select_screen('experiment')
        self.assertEqual(self.shell.current_screen,'experiment')


if __name__ == '__main__':
    unittest.main()
