"""Regression gate for user-facing Polish UI and Manual Index; excludes full guides."""
import re
import unittest
from pytracker_gui.screens import GUI_SETTINGS_TEXTS, GUI_HELP_SHORT_PL, GUI_COLOR_ROLES_PL, POLISH_INDEX_TITLES
from pytracker_gui.logs_screen import TEXTS
from pytracker_gui.parameter_help import parameter_catalog, english_tooltip_catalog
from pytracker_gui.i18n import translate

BAD = re.compile(r'\b(?:Logs|Home|Experiment|Environment|Settings|Sampling rate|Calibration enable|Outer line color|fontu|fixation dot|Model bbox)\b', re.I)

class PolishGuiSeparation(unittest.TestCase):
    def test_setting_strings(self):
        self.assertEqual(set(GUI_SETTINGS_TEXTS['pl']),set(GUI_SETTINGS_TEXTS['en']))
        for key,value in GUI_SETTINGS_TEXTS['pl'].items():
            with self.subTest(key=key): self.assertIsNone(BAD.search(value),value)
    def test_tooltips(self):
        for group in (GUI_HELP_SHORT_PL,GUI_COLOR_ROLES_PL):
            for key,value in group.items():
                with self.subTest(key=key): self.assertIsNone(BAD.search(value),value)
    def test_logs_labels(self):
        self.assertEqual(set(TEXTS['pl']),set(TEXTS['en']))
    def test_index_labels_and_identity(self):
        pl=parameter_catalog(); en=english_tooltip_catalog()
        self.assertEqual(set(pl),set(en))
        for key,item in pl.items():
            with self.subTest(key=key):
                self.assertIsNone(BAD.search(POLISH_INDEX_TITLES.get(key,item['title'])),item['title'])
                self.assertEqual([o['value'] for o in item.get('options',[])],
                                 [o['value'] for o in en[key].get('options',[])])
    def test_field_translation(self):
        for pl,en in [('Poziom rejestrowania','Log level'),('Model obszarów','Bounding box model'),('Wysokość czcionki','Font height')]:
            self.assertEqual(translate(pl,'en'),en)
            self.assertEqual(translate(pl,'pl'),pl)
if __name__ == '__main__': unittest.main()
