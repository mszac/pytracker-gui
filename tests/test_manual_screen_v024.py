"""v0.2.4: documentation navigation stays lazy, local and read-only."""
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from unittest import TestCase, skipUnless
from unittest.mock import patch

from pytracker_gui.parameter_help import parameter_catalog
from tests.test_navigation_shell_v018 import NavigationShellTests


@skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class ManualScreenTests(TestCase):
    setUp = NavigationShellTests.setUp
    tearDown = NavigationShellTests.tearDown

    def test_lazy_manual_and_logo_only(self):
        self.assertNotIn('manual', self.shell.created_screens)
        self.assertFalse(hasattr(self.shell, 'brand_icon'))
        self.assertTrue(self.shell.brand_logo_label.cget('image'))
        self.assertEqual(self.shell.brand_logo_label.cget('style'), 'BrandLogo.TLabel')
        with patch.object(self.gui.runner, 'start', side_effect=AssertionError('No launch')), \
             patch.object(self.gui.runner, 'stop', side_effect=AssertionError('No stop')):
            self.shell.select_screen('manual')
            screen = self.shell._screens['manual']
            self.assertEqual(len(screen.keys), 87)
            self.shell.select_screen('experiment')
            self.shell.select_screen('manual')
            self.assertIs(self.shell._screens['manual'], screen)
            self.assertEqual(tuple(self.shell.nav_buttons)[-2:], ('manual', 'gui-settings'))
            self.shell.open_home()
            self.assertEqual(len(self.shell._screens['home'].tile_buttons), 4)
            self.shell._screens['home'].tile_buttons['manual'].invoke()
            self.assertEqual(self.shell.current_screen, 'manual')

    def test_man_link_opens_exact_extended_record_without_edit_commit(self):
        key = 'display.monitor.width'
        self.gui.tabs.select(self.gui.pages['YAML'])
        self.root.update()
        self.gui.yaml_editor.delete('1.0', 'end')
        self.gui.yaml_editor.insert('1.0', 'unfinished: [')
        self.gui.raw_dirty = True
        with patch.object(self.gui, '_commit_tab', side_effect=AssertionError('Never commit')), \
             patch.object(self.gui.store, 'save', side_effect=AssertionError('Never save')):
            self.gui.info_popover._open_manual(key)
            self.assertEqual(self.shell.current_screen, 'manual')
            manual = self.shell._screens['manual']
            self.assertEqual(manual.current_key, key)
            self.assertIn(parameter_catalog()[key]['long'], manual.details.get('1.0', 'end'))
            self.shell.select_screen('experiment')
            self.assertEqual(self.gui.yaml_editor.get('1.0', 'end-1c'), 'unfinished: [')
            self.assertTrue(self.gui.raw_dirty)

    def test_manual_search_language_deep_link_and_popup_man(self):
        key = 'runtime.log_level'
        self.shell.open_manual(key)
        man = self.shell._screens['manual']
        self.assertEqual(man.current_key, key)
        man.search_var.set('log')
        self.assertLess(len(man.visible_keys), 87)
        man.show_parameter(key)
        self.assertEqual(man.search_var.get(), '')
        self.gui.info_popover.toggle(self.gui._info_icon(self.gui, key), key)
        self.assertTrue(self.gui.info_popover.popup.winfo_exists())
        def descendants(widget):
            for child in widget.winfo_children():
                yield child
                yield from descendants(child)
        links = [w for w in descendants(self.gui.info_popover.popup)
                 if isinstance(w, tk.Label) and w.cget('text') == 'man']
        self.assertEqual(len(links), 1)
        self.assertTrue(links[0].bind('<Button-1>'))
        self.gui.info_popover._open_manual(key)
        self.root.update()
        self.assertIsNone(self.gui.info_popover.popup)
        self.gui.language_name.set('English')
        self.gui._on_language_changed()
        self.assertEqual(man.search_label.cget('text'), 'Search:')
        self.assertIn('Extended description', man.details.get('1.0', 'end'))
        self.assertEqual(man.current_key, key)
        # The manual content tracks help language independently of GUI labels.
        self.gui.help_language_name.set('Polski')
        self.gui._on_help_language_changed()
        self.assertEqual(man.search_label.cget('text'), 'Search:')
        self.assertIn('Opis rozszerzony', man.details.get('1.0', 'end'))
