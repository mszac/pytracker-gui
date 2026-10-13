"""English-only text consistency and GUI Settings manual destinations."""
import unittest
from pathlib import Path
from pytracker_gui.screens import GUI_HELP_SHORT, GUI_COLOR_ROLES, GUI_SETTINGS_TEXTS
from pytracker_gui.theme import COLORS
from pytracker_gui.parameter_help import parameter_catalog, english_tooltip_catalog

ROOT = Path(__file__).resolve().parents[1]

class EnglishHelpAudit(unittest.TestCase):
    def test_all_gui_tooltips_have_unique_manual_targets(self):
        doc = (ROOT / 'docs/GUI_SETTINGS_HELP_V032_EN.md').read_text(encoding='utf-8')
        for key, short in GUI_HELP_SHORT.items():
            self.assertTrue(short.endswith('.'), key)
            self.assertEqual(doc.count('## Option: ' + key + '\n'), 1, key)
        self.assertEqual(set(GUI_COLOR_ROLES), set(COLORS))
        self.assertIn('## Window & appearance', doc)

    def test_english_experiment_catalog_fully_covered(self):
        pl, en = parameter_catalog(), english_tooltip_catalog()
        self.assertEqual(set(pl), set(en))
        for key, record in en.items():
            for field in ('title', 'short', 'long'):
                self.assertTrue(record.get(field, '').strip(), (key, field))

    def test_interface_descriptions_are_english_and_specific(self):
        en = GUI_SETTINGS_TEXTS['en']
        self.assertIn('read-only', en['path_hint'])
        self.assertIn('restart', en['colors_hint'])
        self.assertIn('next launch', en['window_hint'])
