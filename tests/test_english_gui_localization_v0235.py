"""English-only GUI translation regression; documentation deliberately out of scope."""
import ast
import pathlib
import re
import unittest
from pytracker_gui.i18n import UI_EN, FINDING_EN, FINDING_PREFIX_EN, translate

ROOT = pathlib.Path(__file__).resolve().parents[1] / 'pytracker_gui'
POLISH = re.compile(r'[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]|\b(?:Automatyczne|otwieranie|Zapisz|Przywróć|Ścieżki|Ustawienia|Dziennik|Wybierz|Uruchom|Nie udało|Błąd|Brak)\b', re.I)

def named_literal(filename, name):
    tree = ast.parse((ROOT / filename).read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(n, ast.Name) and n.id == name for n in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError(name)

class EnglishGuiAudit(unittest.TestCase):
    def test_gui_settings_keys_and_language(self):
        table = named_literal('screens.py', 'GUI_SETTINGS_TEXTS')
        self.assertEqual(set(table['pl']), set(table['en']))
        for key, value in table['en'].items():
            with self.subTest(key=key):
                self.assertFalse(POLISH.search(value), value)
                self.assertNotEqual(value, table['pl'][key], key)
        self.assertEqual(table['en']['auto_logs'], 'Automatically open Logs')

    def test_logs_history_english(self):
        table = named_literal('logs_screen.py', 'TEXTS')
        self.assertEqual(set(table['pl']), set(table['en']))
        for key, value in table['en'].items():
            with self.subTest(key=key):
                self.assertFalse(POLISH.search(value), value)
                self.assertNotEqual(value, table['pl'][key], key)

    def test_english_translation_values(self):
        for table in (UI_EN, FINDING_EN, FINDING_PREFIX_EN):
            for key, value in table.items():
                with self.subTest(key=key):
                    self.assertFalse(POLISH.search(value), value)
        self.assertEqual(translate('Automatycznie pokazuj logi', 'en'), 'Auto-show logs')

    def test_literal_translated_gui_labels(self):
        for path in ROOT.glob('*.py'):
            tree = ast.parse(path.read_text(encoding='utf-8'))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'translate' and node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    source = node.args[0].value
                    if POLISH.search(source):
                        with self.subTest(file=path.name, line=node.lineno):
                            self.assertFalse(POLISH.search(translate(source, 'en')), source)

if __name__ == '__main__':
    unittest.main()
