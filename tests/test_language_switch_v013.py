"""v0.1.3 UI-only localization: no YAML/profile/runtime semantic change."""
import json
import os
import shutil
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.app import PytrackerGUI
from pytracker_gui.i18n import translate
from pytracker_gui.parameter_help import (english_tooltip_catalog, get_parameter_help,
                                          parameter_catalog)
from pytracker_gui.storage import load_settings, save_settings
from pytracker_gui.yamlconfig import get_value
from tools.render_parameter_manual import render

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent


class TranslationCatalogTests(unittest.TestCase):
    def test_v014_supersedes_short_only_english_docs_without_changing_ui_switch(self):
        source = parameter_catalog()
        translations = english_tooltip_catalog()
        self.assertEqual(len(source), 87)
        self.assertEqual(set(source), set(translations))
        for key in source:
            self.assertTrue(translations[key]['short'].endswith('.'), key)
            self.assertEqual(get_parameter_help(key, 'pl')['short'], source[key]['short'])
            self.assertEqual(get_parameter_help(key, 'en')['short'], translations[key]['short'])
            self.assertEqual(get_parameter_help(key, 'en')['long'], translations[key]['long'])
        self.assertEqual((PROJECT / 'docs/PARAMETER_MANUAL_PL.md').read_text(encoding='utf-8'), render())
        self.assertTrue((PROJECT / 'docs/PARAMETER_MANUAL_EN.md').exists())

    def test_labels_and_form_validation_messages(self):
        self.assertEqual(translate('Język podpowiedzi', 'en'), 'Tooltip language')
        self.assertEqual(translate('Katalog wyników', 'pl'), 'Katalog wyników')
        self.assertEqual(translate('Katalog wyników: wymagana liczba całkowita', 'en'),
                         'Output directory: integer required')
        self.assertIn('Missing', translate('Brak pliku danych: C:/data.csv', 'en'))


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'A display is required')
class LanguageSwitchSmoke(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.upstream = self.home / 'tobii-pytracker'
        self.demo_root = self.upstream / 'tobii-pytracker-demo'
        (self.upstream / 'src/tobii_pytracker').mkdir(parents=True)
        (self.upstream / 'configs').mkdir()
        (self.upstream / 'configs/mouse_eyetracker_config.yaml').write_text('mouse: true\n')
        (self.upstream / 'configs/eyetracker_config.yaml').write_text('tobii: true\n')
        (self.upstream / 'pyproject.toml').write_text('[build-system]\n')
        shutil.copytree(ROOT / 'fixtures/examples', self.demo_root / 'examples')
        (self.demo_root / 'tools').mkdir()
        (self.demo_root / 'tools/run-demo.sh').write_text('#!/bin/bash\n')
        save_settings(self.home, {'demo_root': str(self.demo_root), 'upstream_root': str(self.upstream)})
        self.root = tk.Tk()
        self.root.withdraw()
        self.gui = PytrackerGUI(self.root, home=self.home)
        self.root.update()

    def tearDown(self):
        self.gui.info_popover.dismiss()
        self.root.destroy()
        self.tmp.cleanup()

    def switch_ui(self, name):
        self.gui.language_name.set(name)
        self.gui._on_language_changed()
        self.root.update()

    def switch_help(self, name):
        self.gui.help_language_name.set(name)
        self.gui._on_help_language_changed()
        self.root.update()

    def _popup_words(self):
        def labels(widget):
            result=[]
            for child in widget.winfo_children():
                if isinstance(child, tk.Label): result.append(child.cget('text'))
                result += labels(child)
            return result
        return ' '.join(labels(self.gui.info_popover.popup))

    def test_language_defaults_and_persistence_without_changing_paths(self):
        self.assertEqual(self.gui.language_code, 'pl')
        self.assertEqual(self.gui.help_language_code, 'pl')
        self.switch_ui('English')
        self.assertEqual(self.gui.help_language_code, 'en')
        self.assertEqual(self.gui.tabs.tab(self.gui.pages['Dane'], 'text'), 'Data')
        self.assertEqual(self.gui.tabs.tab(self.gui.pages['Uruchomienie'], 'text'), 'Launch')
        self.assertEqual(self.gui.demo_root.get(), str(self.demo_root))
        settings = load_settings(self.home)
        self.assertEqual(settings['language'], 'en')
        self.assertEqual(settings['help_language'], 'en')
        self.assertEqual(settings['demo_root'], str(self.demo_root))
        self.assertEqual(settings['upstream_root'], str(self.upstream))
        self.root.destroy()
        self.root = tk.Tk()
        self.root.withdraw()
        self.gui = PytrackerGUI(self.root, home=self.home)
        self.root.update()
        self.assertEqual(self.gui.language_code, 'en')
        self.assertEqual(self.gui.tabs.tab(self.gui.pages['Dane'], 'text'), 'Data')
        self.switch_ui('Polski')
        self.assertEqual(self.gui.help_language_code, 'pl')
        self.assertEqual(self.gui.tabs.tab(self.gui.pages['Dane'], 'text'), 'Dane')

    def test_separate_polish_tooltips_with_english_ui(self):
        self.switch_ui('English')
        self.gui._info_icon  # the previously registered controls use the same popup
        self.gui.tabs.select(self.gui.pages['Monitor'])
        self.root.update()
        self.assertEqual(self.gui.field_vars['Monitor']['display.monitor.width'][0].title, 'Szerokość fizyczna (cm)')
        self.assertEqual(self.gui.tabs.tab(self.gui.pages['Monitor'], 'text'), 'Monitor')
        self.assertEqual(self.gui.help_language_code, 'en')
        from pytracker_gui.help_widgets import InfoButton
        def find_buttons(widget):
            res=[]
            for ch in widget.winfo_children():
                if isinstance(ch, InfoButton):res.append(ch)
                res.extend(find_buttons(ch))
            return res
        button=next(i for i in find_buttons(self.gui.pages['Monitor'])
                    if i.help_key == 'display.monitor.width')
        button.invoke()
        self.assertIn(get_parameter_help('display.monitor.width', 'en')['short'], self._popup_words())
        self.switch_help('Polski')
        self.assertEqual(self.gui.language_code, 'en')
        button.invoke()
        self.assertIn(get_parameter_help('display.monitor.width', 'pl')['short'], self._popup_words())
        self.assertTrue(load_settings(self.home)['help_language_explicit'])
        self.switch_ui('Polski')
        self.switch_ui('English')
        self.assertEqual(self.gui.help_language_code, 'pl')

    def test_unsaved_form_value_and_source_yaml_survive_switch(self):
        source = self.demo_root / 'examples/test_demo/config.native.yaml'
        before = source.read_bytes()
        self.gui.tabs.select(self.gui.pages['Monitor'])
        self.root.update()
        self.gui.field_vars['Monitor']['display.monitor.width'][1].set('47.2')
        self.switch_ui('English')
        self.assertEqual(get_value(self.gui.docs['main'], 'display.monitor.width'), 47.2)
        self.assertEqual(self.gui.field_vars['Monitor']['display.monitor.width'][1].get(), '47.2')
        self.assertTrue(self.gui._save())
        self.assertEqual(before, source.read_bytes())
        profile = self.home/'projects/test_en/profiles/test_en/main.yaml'
        self.assertTrue(profile.is_file())
        self.assertIn('47.2', profile.read_text(encoding='utf8'))

    def test_invalid_yaml_does_not_disappear_when_language_changes(self):
        self.gui.tabs.select(self.gui.pages['YAML'])
        self.root.update()
        self.gui.yaml_editor.delete('1.0', 'end')
        self.gui.yaml_editor.insert('1.0', 'foo: [not valid')
        self.gui.raw_dirty = True
        with patch('pytracker_gui.app.messagebox.showerror') as dialog:
            self.switch_ui('English')
        self.assertTrue(dialog.called)
        self.assertEqual(self.gui.language_code, 'pl')
        self.assertEqual(self.gui.yaml_editor.get('1.0', 'end-1c'), 'foo: [not valid')

    def test_help_language_does_not_rewrite_profile_or_manual(self):
        source = (PROJECT / 'docs/PARAMETER_MANUAL_PL.md').read_bytes()
        self.switch_help('English')
        self.assertEqual(self.gui.language_code, 'pl')
        self.assertEqual(self.gui.help_language_code, 'en')
        self.assertEqual((PROJECT / 'docs/PARAMETER_MANUAL_PL.md').read_bytes(), source)
        self.assertEqual(self.gui.gaze.get(), 'mouse')
        self.assertFalse((self.home/'profiles').exists())


if __name__ == '__main__':
    unittest.main()
