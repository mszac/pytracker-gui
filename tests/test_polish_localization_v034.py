"""Polish help parity with English baseline; no experiment execution."""
import unittest
from pathlib import Path
from pytracker_gui.screens import GUI_HELP_SHORT, GUI_HELP_SHORT_PL, GUI_COLOR_ROLES
from pytracker_gui.parameter_help import parameter_catalog, english_tooltip_catalog, get_parameter_help
from pytracker_gui.gui_docs import discover_gui_documents
from tools.render_parameter_manual import render

ROOT = Path(__file__).resolve().parents[1]

class PolishLocalizationTests(unittest.TestCase):
    def test_tooltip_keys_complete(self):
        self.assertEqual(set(GUI_HELP_SHORT_PL), set(GUI_HELP_SHORT))
        for key, value in GUI_HELP_SHORT_PL.items():
            self.assertGreater(len(value), 20, key)
            self.assertTrue(value.endswith('.'), key)

    def test_gui_manual_topics_complete_in_both_languages(self):
        for lang in ('EN', 'PL'):
            text = (ROOT / f'docs/GUI_SETTINGS_HELP_V032_{lang}.md').read_text()
            for key in GUI_HELP_SHORT:
                self.assertEqual(text.count(('## Opcja: ' if lang == 'PL' else '## Option: ') + key + '\n'), 1, (lang,key))

    def test_options_english_polish_identical_ids_and_values(self):
        en = english_tooltip_catalog()
        pl = parameter_catalog()
        self.assertEqual(set(en), set(pl))
        count = 0
        for key in en:
            pe = pl[key].get('options', [])
            ee = en[key].get('options', [])
            self.assertEqual([o['value'] for o in pe], [o['value'] for o in ee], key)
            for item in pe:
                self.assertTrue(item['description'].strip(),key)
            count += len(pe)
        self.assertEqual(count, 70)
        self.assertIn('**Dostępne wartości:**', render('pl'))

    def test_polish_gui_guide_discovered(self):
        docs = discover_gui_documents(ROOT)
        flattened = str(docs)
        self.assertIn('GUI_SETTINGS_HELP_V032_PL.md',flattened)
        self.assertIn('GUI_SETTINGS_HELP_V032_EN.md',flattened)

if __name__ == '__main__': unittest.main()
