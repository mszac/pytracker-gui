"""v0.2.17: Environment column-only equal widths; lazy bundled GUI docs."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.gui_docs import discover_gui_documents, MAX_GUI_DOC_BYTES


class GuiDocsFileTests(unittest.TestCase):
    def test_current_and_feature_docs_only_in_this_gui_install(self):
        root = Path(__file__).resolve().parents[1]
        docs = discover_gui_documents(root)
        self.assertEqual(set(docs), {'en', 'pl'})
        for lang in ('en', 'pl'):
            current = {r for _, r, _ in docs[lang]['current']}
            self.assertIn(f'docs/USER_GUIDE_{lang.upper()}.md', current)
            self.assertIn(f'README_WINDOWS_GIT_BASH_{lang.upper()}.md', current)
            self.assertIn('README.md', current)
            feature = {r for _, r, _ in docs[lang]['features']}
            self.assertIn(f'docs/GUI_DOCUMENTATION_V0217_{lang.upper()}.md', feature)
            for section in docs[lang].values():
                for _, _, path in section:
                    self.assertTrue(path.is_relative_to(root.resolve()))
                    self.assertNotIn('logs', path.parts)
                    self.assertNotIn('adr', path.parts)
                    self.assertNotIn('experiments', path.parts)
        self.assertEqual(MAX_GUI_DOC_BYTES, 1024 * 1024)

    def test_missing_files_and_symlinks_never_in_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'docs').mkdir()
            (root/'docs/USER_GUIDE_EN.md').write_text('# English')
            (root/'README.md').write_text('# Overview')
            (root/'logs').mkdir()
            (root/'logs/secret.md').write_text('do not read')
            (root/'docs/USER_GUIDE_PL.md').symlink_to(root/'logs/secret.md')
            docs=discover_gui_documents(root)
            paths={rel for sections in docs.values() for entries in sections.values()
                   for _,rel,_ in entries}
            self.assertIn('docs/USER_GUIDE_EN.md',paths)
            self.assertNotIn('docs/USER_GUIDE_PL.md',paths)
            self.assertNotIn('logs/secret.md',paths)


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name=='nt','Tk display required')
class GuiDocsTkTests(unittest.TestCase):
    def setUp(self):
        from tests.test_navigation_shell_v018 import NavigationShellTests
        NavigationShellTests.setUp(self)
        self.nav = NavigationShellTests

    def tearDown(self):
        self.nav.tearDown(self)

    def _env_buttons(self):
        env=self.gui.grid_slaves(row=1,column=0)[0]
        return [env.grid_slaves(row=i,column=3)[0] for i in range(4)]

    def test_equal_only_widths_without_layout_style_icon_changes(self):
        buttons=self._env_buttons()
        self.root.deiconify();self.root.update_idletasks();self.root.update()
        sizes=[(b.winfo_width(),b.winfo_height()) for b in buttons]
        self.assertEqual(len({w for w,h in sizes}),1,sizes)
        self.assertEqual([b.cget('style') for b in buttons],['']*4)
        self.assertTrue(all(b.grid_info().get('sticky')=='ew' for b in buttons))
        self.assertEqual([b.grid_info().get('padx') for b in buttons],[6,6,6,6])
        self.assertEqual([b.cget('text') for b in buttons],
                         ['Zapisz ścieżki','Sprawdź Python','Wczytaj repo','Wykryj układ'])
        self.assertTrue(all(b.cget('image') for b in buttons))
        self.gui.language_name.set('English');self.gui._on_language_changed();self.root.update()
        self.assertEqual(len({b.winfo_width() for b in buttons}),1)

    def test_fourth_tab_lazy_tree_read_only_and_deeplink(self):
        from pytracker_gui.theme import COLORS
        from tkinter import ttk
        self.shell.select_screen('manual')
        man=self.shell._screens['manual']
        self.assertEqual(len(man.tabs.tabs()),4)
        self.assertEqual(man.tabs.select(),str(man.index_page))
        self.assertIsNone(man._gui_docs_view)
        with patch.object(self.gui.runner,'start',side_effect=AssertionError('do not launch')):
            man.tabs.select(man.gui_documentation_page);self.root.update()
        view=man._gui_docs_view
        self.assertIsNotNone(view)
        self.assertTrue({'en','pl'}.issubset(view.groups))
        self.assertEqual(view.text.cget('state'),'disabled')
        self.assertEqual(view.tree.cget('style'),'GuiDocs.Treeview')
        style=ttk.Style(self.root)
        self.assertEqual(style.lookup('GuiDocs.Treeview','background'),COLORS['field'])
        self.assertEqual(style.lookup('GuiDocs.Treeview','foreground'),COLORS['text'])
        self.assertEqual(style.lookup('GuiDocs.Treeview','foreground',('selected',)),COLORS['accent_text'])
        view.select_file('docs/USER_GUIDE_PL.md')
        self.assertIn('pytracker-gui v0.2.17',view.text.get('1.0','end'))
        self.assertTrue(view.text.tag_ranges('doc_h1'))
        self.assertEqual(view.text.cget('state'),'disabled')
        man.show_parameter('gui.gaze')
        self.assertEqual(man.tabs.select(),str(man.index_page))
        self.assertEqual(man.current_key,'gui.gaze')

    def test_unsaved_yaml_preserved_and_changed_language(self):
        self.gui.tabs.select(self.gui.pages['YAML']);self.root.update()
        self.gui.yaml_editor.delete('1.0','end');self.gui.yaml_editor.insert('1.0','bad: [')
        self.gui.raw_dirty=True
        with patch.object(self.gui,'_commit_tab',side_effect=AssertionError('No YAML commit')), \
             patch.object(self.gui.store,'save',side_effect=AssertionError('No project writes')):
            self.shell.select_screen('manual')
            man=self.shell._screens['manual'];man.tabs.select(man.gui_documentation_page)
            self.root.update()
            view=man._gui_docs_view
            view.select_file('docs/DOCUMENTATION_INDEX_EN.md')
            man.set_language('en')
            self.assertEqual(man.tabs.select(),str(man.gui_documentation_page))
            self.assertIs(view,man._gui_docs_view)
            self.assertEqual(view.current_file,'docs/DOCUMENTATION_INDEX_EN.md')
            self.assertEqual(view.status.cget('text'), 'Local pytracker-gui documentation (read-only)')
            self.shell.select_screen('experiment')
            self.assertEqual(self.gui.yaml_editor.get('1.0','end-1c'),'bad: [')
            self.assertTrue(self.gui.raw_dirty)

    def test_bounded_read_and_missing_immutable_file(self):
        from pytracker_gui.gui_docs import GuiDocumentationBrowser
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'docs').mkdir()
            file=root/'docs/USER_GUIDE_EN.md';file.write_text('Z'*(MAX_GUI_DOC_BYTES+1))
            browser=GuiDocumentationBrowser(self.root,language='en',project_root=root)
            browser.select_file('docs/USER_GUIDE_EN.md')
            self.assertIn('exceeds the 1 MiB',browser.text.get('1.0','end'))
            file.unlink()
            browser.select_file('docs/USER_GUIDE_EN.md')
            self.assertIn('Cannot read',browser.text.get('1.0','end'))
            browser.destroy()


if __name__=='__main__':unittest.main()
