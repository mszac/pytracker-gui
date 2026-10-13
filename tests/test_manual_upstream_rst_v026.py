"""v0.2.6: distinct Index / local upstream RST Documentation tabs, no launcher edits."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.upstream_docs import discover_rst_files, MAX_RST_BYTES
from pytracker_gui.theme import COLORS


class UpstreamRstFileTests(unittest.TestCase):
    def test_only_upstream_rst_nested_documents_and_no_demo_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'docs/guides').mkdir(parents=True)
            (root / 'docs/index.rst').write_text('Index\n=====\n', encoding='utf-8')
            (root / 'docs/guides/calibration.rst').write_text('Calibrate\n=========\n', encoding='utf-8')
            (root / 'docs/readme.md').write_text('# not rst', encoding='utf-8')
            (root / 'tobii-pytracker-demo/docs').mkdir(parents=True)
            (root / 'tobii-pytracker-demo/docs/demo.rst').write_text('Not upstream')
            self.assertEqual([name for name, _ in discover_rst_files(root)],
                             ['guides/calibration.rst', 'index.rst'])
            self.assertEqual(discover_rst_files(root / 'missing'), [])

    def test_reader_rejects_escaping_symlinks_if_supported(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'docs').mkdir()
            (root / 'outside.rst').write_text('outside')
            try:
                (root / 'docs/escape.rst').symlink_to(root / 'outside.rst')
            except (OSError, NotImplementedError):
                self.skipTest('filesystem does not permit symlinks')
            self.assertEqual(discover_rst_files(root), [])
            self.assertEqual(MAX_RST_BYTES, 2 * 1024 * 1024)


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class ManualUpstreamTkTests(unittest.TestCase):
    def setUp(self):
        from tests.test_navigation_shell_v018 import NavigationShellTests
        NavigationShellTests.setUp(self)
        self.upstream_root = Path(self.gui.upstream.get())
        self.docs = self.upstream_root / 'docs'
        (self.docs / 'tutorials').mkdir(parents=True)
        (self.docs / 'index.rst').write_text('Welcome\n=======\n\n.. toctree::\n\n   tutorials/configuration\n', encoding='utf-8')
        (self.docs / 'tutorials/configuration.rst').write_text(
            'Configuration\n=============\n\nUse this example.\n', encoding='utf-8')
        (self.upstream_root / 'tobii-pytracker-demo/docs').mkdir(parents=True)
        (self.upstream_root / 'tobii-pytracker-demo/docs/demo.rst').write_text('Excluded')

    def tearDown(self):
        from tests.test_navigation_shell_v018 import NavigationShellTests
        NavigationShellTests.tearDown(self)

    def test_lazy_documentation_index_default_and_green_option_values(self):
        self.shell.select_screen('manual')
        manual = self.shell._screens['manual']
        self.assertEqual(manual.tabs.select(), str(manual.index_page))
        self.assertIsNone(manual._docs_view)
        self.assertEqual(manual.tabs.tab(manual.index_page, 'text'), 'Index')
        self.assertEqual(manual.tabs.tab(manual.documentation_page, 'text'), 'Documentation')
        manual.set_language('en', 'en')
        manual.show_parameter('gui.gaze')
        self.assertIn('MOUSEGAZE', manual.details.get('1.0', 'end'))
        self.assertEqual(manual.details.tag_cget('option_value', 'foreground'), COLORS['success'])
        self.assertNotEqual(manual.details.tag_cget('head', 'foreground'), COLORS['success'])
        self.assertTrue(manual.details.tag_ranges('option_value'))
        with patch.object(self.gui.runner, 'start', side_effect=AssertionError('do not launch')):
            manual.tabs.select(manual.documentation_page)
            self.root.update()
        self.assertIsNotNone(manual._docs_view)
        self.assertEqual(set(manual._docs_view.documents), {'index.rst', 'tutorials/configuration.rst'})
        manual._docs_view.select_file('tutorials/configuration.rst')
        self.assertIn('Use this example.', manual._docs_view.text.get('1.0', 'end'))
        self.assertNotIn('demo.rst', manual._docs_view.documents)

    def test_popup_deep_link_returns_to_index_and_preserves_invalid_unsaved_yaml(self):
        self.gui.tabs.select(self.gui.pages['YAML'])
        self.root.update()
        self.gui.yaml_editor.delete('1.0', 'end')
        self.gui.yaml_editor.insert('1.0', 'bad: [')
        self.gui.raw_dirty = True
        self.shell.select_screen('manual')
        man = self.shell._screens['manual']
        man.tabs.select(man.documentation_page)
        self.root.update()
        with patch.object(self.gui, '_commit_tab', side_effect=AssertionError('no commit')), \
             patch.object(self.gui.store, 'save', side_effect=AssertionError('no save')):
            self.shell.open_manual('display.monitor.width')
            self.assertEqual(man.tabs.select(), str(man.index_page))
            self.assertEqual(man.current_key, 'display.monitor.width')
            self.shell.select_screen('experiment')
            self.assertEqual(self.gui.yaml_editor.get('1.0', 'end-1c'), 'bad: [')
            self.assertTrue(self.gui.raw_dirty)

    def test_documentation_read_only_language_and_missing_files(self):
        self.shell.select_screen('manual')
        man = self.shell._screens['manual']
        man.tabs.select(man.documentation_page)
        self.root.update()
        browser = man._docs_view
        self.assertIn('index.rst', browser.documents)
        browser.select_file('index.rst')
        self.assertIn('.. toctree::', browser.text.get('1.0', 'end'))
        self.assertEqual(browser.text.cget('state'), 'disabled')
        self.gui.language_name.set('English')
        self.gui._on_language_changed()
        self.assertEqual(browser.filter_label.cget('text'), 'Filter files:')
        self.assertEqual(man.tabs.select(), str(man.documentation_page))
        # A newly selected source root refreshes documents only on Documentation activation.
        other = self.upstream_root / 'new-upstream'
        (other / 'docs').mkdir(parents=True)
        (other / 'docs/new.rst').write_text('New\n===\n')
        self.gui.upstream.set(str(other))
        man.tabs.select(man.index_page)
        self.root.update()
        self.assertIn('index.rst', browser.documents)
        man.tabs.select(man.documentation_page)
        self.root.update()
        self.assertEqual(set(browser.documents), {'new.rst'})


if __name__ == '__main__':
    unittest.main()
