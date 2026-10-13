"""v0.3.0: navigation removal, lazy project Markdown tree, lightweight document viewer."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.demo_docs import discover_demo_markdown, MAX_MD_BYTES
from pytracker_gui.shell import SCREEN_IDS


class DemoDocsSourceTests(unittest.TestCase):
    def test_project_scoped_markdown_and_safe_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'examples/ux_ab_demo').mkdir(parents=True)
            (root / 'examples/test_demo').mkdir(parents=True)
            (root / 'docs/basic_examples').mkdir(parents=True)
            (root / 'examples/ux_ab_demo/README.md').write_text('# UX')
            (root / 'examples/ux_ab_demo/EXPERIMENT.md').write_text('# Study')
            (root / 'docs/basic_examples/ux_ab_text_demo.md').write_text('# Guide')
            (root / 'examples/test_demo/README.md').write_text('# Test')
            (root / 'docs/README.md').write_text('# Unrelated')
            (root / 'output').mkdir()
            (root / 'output/log.md').write_text('Sensitive')
            outside = root.parent / 'external-notes-test.md'
            try:
                (root / 'examples/ux_ab_demo/external.md').symlink_to(outside)
            except (OSError, NotImplementedError):
                pass
            groups = discover_demo_markdown(root)
            self.assertEqual(set(groups), {'ux_ab_demo', 'test_demo'})
            ux_names = [name for name, _ in groups['ux_ab_demo']]
            self.assertIn('README.md', ux_names)
            self.assertIn('Guide / ux_ab_text_demo.md', ux_names)
            self.assertNotIn('external.md', ux_names)
            self.assertTrue(all('output' not in str(path) for files in groups.values() for _, path in files))
            self.assertEqual(discover_demo_markdown(root / 'missing'), {})
            self.assertEqual(MAX_MD_BYTES, 1024 * 1024)

    def test_diagnostics_removed_from_main_navigation(self):
        self.assertNotIn('diagnostics', SCREEN_IDS)


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt', 'Tk display required')
class DemoDocsTkTests(unittest.TestCase):
    def setUp(self):
        from tests.test_navigation_shell_v018 import NavigationShellTests
        NavigationShellTests.setUp(self)
        self.demo_root = Path(self.gui.demo_root.get())
        (self.demo_root / 'examples/test_demo/README.md').write_text(
            '# Test Project\n\n## Workflow\n\n- Select stimulus\n- Click **Start**\n\n```bash\npython run.py\n```\n', encoding='utf-8')
        (self.demo_root / 'examples/ux_ab_demo/README.md').write_text('# UX Project\n', encoding='utf-8')
        self.shell.select_screen('manual')
        self.manual = self.shell._screens['manual']

    def tearDown(self):
        from tests.test_navigation_shell_v018 import NavigationShellTests
        NavigationShellTests.tearDown(self)

    def test_demo_browser_lazy_and_tree_and_rendering(self):
        self.assertEqual(self.manual.tabs.select(), str(self.manual.index_page))
        self.assertIsNone(self.manual._demo_view)
        with patch.object(self.gui.runner, 'start', side_effect=AssertionError('no process')):
            self.manual.tabs.select(self.manual.demo_documentation_page)
            self.root.update()
        browser = self.manual._demo_view
        self.assertIsNotNone(browser)
        self.assertIn('test_demo', browser.groups)
        self.assertIn('ux_ab_demo', browser.groups)
        self.assertEqual(len(browser.tree.get_children('')), 2)
        self.assertEqual(browser.text.cget('state'), 'disabled')
        readme = self.demo_root / 'examples/test_demo/README.md'
        browser.select_file(readme.resolve())
        rendered = browser.text.get('1.0', 'end')
        self.assertIn('Test Project', rendered)
        self.assertNotIn('# Test Project', rendered)
        self.assertIn('python run.py', rendered)
        self.assertTrue(browser.text.tag_ranges('doc_h1'))
        self.assertTrue(browser.text.tag_ranges('doc_code'))
        self.assertIs(self.manual._demo_view, browser)


    def test_demo_tree_has_dark_background_and_readable_selection(self):
        from tkinter import ttk
        from pytracker_gui.theme import COLORS
        self.manual.tabs.select(self.manual.demo_documentation_page)
        self.root.update()
        browser = self.manual._demo_view
        self.assertEqual(browser.tree.cget('style'), 'DemoDocs.Treeview')
        style = ttk.Style(self.root)
        name = browser.tree.cget('style')
        self.assertEqual(style.lookup(name, 'background'), COLORS['field'])
        self.assertEqual(style.lookup(name, 'fieldbackground'), COLORS['field'])
        self.assertEqual(style.lookup(name, 'foreground'), COLORS['text'])
        self.assertEqual(style.lookup(name, 'background', ('selected',)), COLORS['selection'])
        self.assertEqual(style.lookup(name, 'foreground', ('selected',)), COLORS['accent_text'])

    def test_manual_deep_link_returns_to_index_and_preserves_yaml(self):
        self.gui.tabs.select(self.gui.pages['YAML'])
        self.root.update()
        self.gui.yaml_editor.delete('1.0', 'end')
        self.gui.yaml_editor.insert('1.0', 'bad: [')
        self.gui.raw_dirty = True
        self.manual.tabs.select(self.manual.demo_documentation_page)
        self.root.update()
        with patch.object(self.gui, '_commit_tab', side_effect=AssertionError('no YAML commits')), \
             patch.object(self.gui.runner, 'stop', side_effect=AssertionError('no stop')):
            self.shell.open_manual('gui.gaze')
            self.assertEqual(self.manual.tabs.select(), str(self.manual.index_page))
            self.assertEqual(self.manual.current_key, 'gui.gaze')
            self.shell.select_screen('experiment')
            self.assertEqual(self.gui.yaml_editor.get('1.0', 'end-1c'), 'bad: [')

    def test_demo_root_change_only_on_tab_activation(self):
        self.manual.tabs.select(self.manual.demo_documentation_page)
        self.root.update()
        browser = self.manual._demo_view
        old_root = browser.repository_root
        another = self.demo_root.parent / 'another-demo'
        (another / 'examples/any_project').mkdir(parents=True)
        (another / 'examples/any_project/README.md').write_text('# Other')
        self.gui.demo_root.set(str(another))
        self.manual.tabs.select(self.manual.index_page)
        self.root.update()
        self.assertEqual(browser.repository_root, old_root)
        self.manual.tabs.select(self.manual.demo_documentation_page)
        self.root.update()
        self.assertEqual(browser.repository_root, another.resolve())
        self.assertEqual(set(browser.groups), {'any_project'})


if __name__ == '__main__':
    unittest.main()
