"""Lazy, read-only tree browser for Markdown instructions in demo projects.

Only local <demo_root>/examples/<project>/**/*.md and a matching optional
<demo_root>/docs/basic_examples/<project-guide>.md are eligible. No project
outputs, private run logs, upstream RST, network, or directory writes.
"""
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk

from .document_render import configure_document_tags, render_document
from .theme import COLORS

MAX_MD_BYTES = 1024 * 1024
MAX_PROJECTS = 64
MAX_FILES = 256
# Public guide filenames from the demo repository; folders are discovered dynamically.
_GUIDES = {
    'test_demo': None,
    'ux_ab_demo': 'ux_ab_text_demo.md',
    'timeseries_noise_demo': 'timeseries_noise_demo.md',
    'text_search_demo': 'text_search_demo.md',
    'image_semantic_demo': 'image_semantic_demo.md',
}


def discover_demo_markdown(demo_root):
    """Map project folder -> [(relative label, absolute path)]; symlink-safe."""
    root = Path(demo_root).expanduser().resolve()
    examples = root / 'examples'
    if not examples.is_dir():
        return {}
    groups = {}
    count = 0
    for project in sorted(examples.iterdir(), key=lambda p: p.name.casefold()):
        if len(groups) >= MAX_PROJECTS or count >= MAX_FILES:
            break
        if project.is_symlink() or not project.is_dir():
            continue
        docs = []
        # Filesystem traversal does not follow symlinks or leave the project root.
        for base, dirs, names in os.walk(project, followlinks=False):
            dirs[:] = sorted(d for d in dirs if not (Path(base) / d).is_symlink())
            for name in sorted(names):
                if count + len(docs) >= MAX_FILES:
                    break
                path = Path(base) / name
                if path.suffix.lower() != '.md' or path.is_symlink() or not path.is_file():
                    continue
                resolved = path.resolve()
                if resolved.is_relative_to(project.resolve()):
                    docs.append((path.relative_to(project).as_posix(), resolved))
            if count + len(docs) >= MAX_FILES:
                break
        guide_name = _GUIDES.get(project.name)
        if guide_name and count + len(docs) < MAX_FILES:
            guide = root / 'docs' / 'basic_examples' / guide_name
            if guide.is_file() and not guide.is_symlink() and guide.resolve().is_relative_to(root):
                docs.append((f'Guide / {guide_name}', guide.resolve()))
        if docs:
            groups[project.name] = sorted(docs, key=lambda item: item[0].casefold())
            count += len(docs)
    return groups


class DemoProjectDocsBrowser(ttk.Frame):
    """Tree navigation with project nodes and Markdown leaves; load on selection."""
    def __init__(self, master, demo_root_provider, language='pl'):
        super().__init__(master, padding=8)
        self.demo_root_provider = demo_root_provider
        self.language = language
        self.repository_root = None
        self.groups = {}
        self.node_paths = {}
        self.current_file = None
        self.status = ttk.Label(self, style='Muted.TLabel')
        self.status.pack(anchor='w', pady=(0, 8))
        panes = ttk.Panedwindow(self, orient='horizontal')
        panes.pack(fill='both', expand=True)
        left = ttk.Frame(panes)
        right = ttk.Frame(panes)
        panes.add(left, weight=1)
        panes.add(right, weight=3)
        # Native ttk's actual base style is "Treeview" (not "TTreeview").
        # Give this browser an explicit dark style so Windows never renders
        # light tree rows underneath our light text.
        style = ttk.Style(self)
        style.configure('DemoDocs.Treeview', background=COLORS['field'],
                        fieldbackground=COLORS['field'], foreground=COLORS['text'],
                        rowheight=27, bordercolor=COLORS['border'])
        style.map('DemoDocs.Treeview',
                  background=[('selected', COLORS['selection'])],
                  foreground=[('selected', COLORS['accent_text'])])
        self.tree = ttk.Treeview(left, show='tree', selectmode='browse',
                                 style='DemoDocs.Treeview')
        tree_scroll = ttk.Scrollbar(left, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
        self.tree.bind('<<TreeviewSelect>>', self._selected)
        self.text = tk.Text(right, wrap='word', state='disabled', relief='flat',
                            borderwidth=0, padx=16, pady=12,
                            background=COLORS['field'], foreground=COLORS['text'])
        scroll = ttk.Scrollbar(right, orient='vertical', command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        self.text.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        configure_document_tags(self.text)
        self.set_language(language)
        self.refresh_repository_if_changed()

    def _msg(self, pl, en):
        return en if self.language == 'en' else pl

    def set_language(self, language):
        self.language = language
        self._update_status()
        if self.current_file is None:
            self._empty()

    def _update_status(self):
        if self.repository_root is None:
            return
        self.status.configure(text=self._msg('Instrukcje projektów startowych: ',
                                             'Starter-project instructions: ') +
                              str(self.repository_root / 'examples'))

    def refresh_repository_if_changed(self):
        root = Path(self.demo_root_provider()).expanduser().resolve()
        if root == self.repository_root:
            return
        self.repository_root = root
        self.groups = discover_demo_markdown(root)
        self.node_paths.clear()
        self.current_file = None
        self.tree.delete(*self.tree.get_children(''))
        for project, documents in self.groups.items():
            parent = self.tree.insert('', 'end', text=project.replace('_', ' '), open=True)
            for label, path in documents:
                node = self.tree.insert(parent, 'end', text=label)
                self.node_paths[node] = path
        self._update_status()
        self._empty()

    def _empty(self):
        message = self._msg('Wybierz plik Markdown w drzewie projektów.' if self.groups else
                            'Nie znaleziono instrukcji Markdown w katalogu examples/ repozytorium dem.',
                            'Choose a Markdown document in the project tree.' if self.groups else
                            'No Markdown instructions found under the demo repository examples/.')
        self.text.configure(state='normal')
        self.text.delete('1.0', 'end')
        self.text.insert('end', message)
        self.text.configure(state='disabled')

    def _selected(self, _event=None):
        selection = self.tree.selection()
        if not selection:
            return
        path = self.node_paths.get(selection[0])
        if path is None:  # a project/group node, not a file
            self.current_file = None
            self._empty()
            return
        self.select_file(path)

    def select_file(self, path):
        """Load only files from the current tree, rejecting replaced symlinks."""
        requested = Path(path)
        if requested not in self.node_paths.values():
            raise KeyError(str(path))
        self.current_file = requested
        try:
            if requested.is_symlink() or not requested.resolve().is_relative_to(self.repository_root):
                raise OSError('Document is outside the demo repository')
            if requested.stat().st_size > MAX_MD_BYTES:
                raise OSError('Markdown document exceeds the 1 MiB viewer limit')
            value = requested.read_text(encoding='utf-8', errors='replace')
        except OSError as exc:
            self.text.configure(state='normal')
            self.text.delete('1.0', 'end')
            self.text.insert('end', self._msg('Nie można odczytać dokumentu: ',
                                             'Cannot read document: ') + str(exc))
            self.text.configure(state='disabled')
            return
        render_document(self.text, value, 'md')
