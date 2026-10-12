"""Lazy, local, read-only browser for original tobii-pytracker docs/*.rst.

No browser engine, network, external RST renderer, subprocess, timer or extra package.
The original upstream checkout is the sole document authority; demo documentation
is deliberately excluded. Source RST remains verbatim, with lightweight headings.
"""
from pathlib import Path
import tkinter as tk
from tkinter import ttk

from .theme import COLORS
from .document_render import configure_document_tags, render_document

MAX_RST_BYTES = 2 * 1024 * 1024
HEADING_RULES = frozenset('=-~^"`:+*#')


def discover_rst_files(upstream_root):
    """Return safe local documents (relative path, absolute path), sorted by name."""
    base = Path(upstream_root).expanduser().resolve() / 'docs'
    if not base.is_dir():
        return []
    result = []
    for path in base.rglob('*.rst'):
        if path.is_symlink() or not path.is_file():
            continue
        resolved = path.resolve()
        if not resolved.is_relative_to(base):
            continue
        result.append((path.relative_to(base).as_posix(), resolved))
    return sorted(result, key=lambda entry: (entry[0].casefold(), entry[0]))


class UpstreamRstBrowser(ttk.Frame):
    """One on-demand doc list, one on-demand file reader, no background work."""

    def __init__(self, master, upstream_root_provider, language='pl'):
        super().__init__(master, padding=8)
        self.upstream_root_provider = upstream_root_provider
        self.language = language
        self.repository_root = None
        self.documents = {}
        self.visible_paths = []
        self.current_path = None
        self.status_label = ttk.Label(self, style='Muted.TLabel')
        self.status_label.pack(anchor='w', pady=(0, 7))
        self.filter_var = tk.StringVar(self)
        line = ttk.Frame(self)
        line.pack(fill='x', pady=(0, 8))
        self.filter_label = ttk.Label(line)
        self.filter_label.pack(side='left', padx=(0, 8))
        self.filter_entry = ttk.Entry(line, textvariable=self.filter_var)
        self.filter_entry.pack(side='left', fill='x', expand=True)
        self.filter_var.trace_add('write', self._filter_changed)
        panes = ttk.Panedwindow(self, orient='horizontal')
        panes.pack(fill='both', expand=True)
        names = ttk.Frame(panes)
        view = ttk.Frame(panes)
        panes.add(names, weight=1)
        panes.add(view, weight=3)
        self.files = tk.Listbox(names, exportselection=False, font=('TkDefaultFont', 10),
                                relief='flat', borderwidth=0, activestyle='none',
                                background=COLORS['field'], foreground=COLORS['text'],
                                selectbackground=COLORS['selection'],
                                selectforeground=COLORS['accent_text'], highlightthickness=0)
        file_scroll = ttk.Scrollbar(names, orient='vertical', command=self.files.yview)
        self.files.configure(yscrollcommand=file_scroll.set)
        self.files.pack(side='left', fill='both', expand=True)
        file_scroll.pack(side='right', fill='y')
        self.files.bind('<<ListboxSelect>>', self._selected)
        self.text = tk.Text(view, wrap='word', state='disabled', relief='flat',
                            borderwidth=0, padx=16, pady=13,
                            font=('TkFixedFont', 10), background=COLORS['field'],
                            foreground=COLORS['text'], insertbackground=COLORS['text'])
        doc_scroll = ttk.Scrollbar(view, orient='vertical', command=self.text.yview)
        self.text.configure(yscrollcommand=doc_scroll.set)
        self.text.pack(side='left', fill='both', expand=True)
        doc_scroll.pack(side='right', fill='y')
        configure_document_tags(self.text)
        self.set_language(language)
        self.refresh_repository_if_changed()

    def _msg(self, pl, en):
        return en if self.language == 'en' else pl

    def set_language(self, language):
        self.language = language
        self.filter_label.configure(text=self._msg('Filtruj pliki:', 'Filter files:'))
        self._set_status()
        if self.current_path is None:
            self._empty_message()

    def _set_status(self):
        if self.repository_root is None:
            return
        if not self.documents:
            self.status_label.configure(text=self._msg(
                'Brak dokumentacji .rst w oryginalnym repozytorium: ',
                'No .rst documentation in the original repository: ') +
                str(self.repository_root / 'docs'))
        else:
            self.status_label.configure(text=self._msg('Dokumentacja upstream: ',
                                                       'Upstream documentation: ') +
                                        str(self.repository_root / 'docs'))

    def refresh_repository_if_changed(self):
        """Check repository path only on actual Documentation tab selection."""
        root = Path(self.upstream_root_provider()).expanduser().resolve()
        if root == self.repository_root:
            return
        self.repository_root = root
        self.documents = dict(discover_rst_files(root))
        self.current_path = None
        self.filter_var.set('')
        self._set_status()
        self._filter_changed()

    def _filter_changed(self, *_args):
        needle = self.filter_var.get().strip().casefold()
        self.visible_paths = [name for name in self.documents if needle in name.casefold()]
        self.files.delete(0, 'end')
        for name in self.visible_paths:
            self.files.insert('end', name)
        if self.current_path in self.visible_paths:
            index = self.visible_paths.index(self.current_path)
            self.files.selection_set(index)
            self.files.see(index)
        elif self.visible_paths:
            self.current_path = self.visible_paths[0]
            self.files.selection_set(0)
            self._show_current()
        else:
            self.current_path = None
            self._empty_message()

    def _selected(self, _event=None):
        selected = self.files.curselection()
        if selected and selected[0] < len(self.visible_paths):
            path = self.visible_paths[selected[0]]
            if path != self.current_path:
                self.current_path = path
                self._show_current()

    def select_file(self, relative_path):
        """Programmatic selection for tests; does not access non-indexed paths."""
        if relative_path not in self.documents:
            raise KeyError(relative_path)
        self.filter_var.set('')
        self.current_path = relative_path
        self._filter_changed()
        self._show_current()

    def _empty_message(self):
        self._display(self._msg('Wybierz plik .rst z listy.' if self.documents else
                                'Nie znaleziono plików .rst w katalogu docs/ oryginalnego tobii-pytracker.',
                                'Select an .rst file from the list.' if self.documents else
                                'No .rst files found in the original tobii-pytracker docs/ directory.'))

    def _display(self, value, is_rst=False):
        self.text.configure(state='normal')
        self.text.delete('1.0', 'end')
        if is_rst:
            render_document(self.text, value, 'rst')
        else:
            self.text.insert('end', value)
            self.text.configure(state='disabled')
        self.text.yview_moveto(0)

    def _show_current(self):
        if self.current_path is None:
            self._empty_message()
            return
        file_path = self.documents[self.current_path]
        try:
            # Validate again at read time so no replaced symlink escapes upstream docs.
            docs_root = (self.repository_root / 'docs').resolve()
            if file_path.is_symlink() or not file_path.resolve().is_relative_to(docs_root):
                raise OSError('Document is outside the upstream docs directory')
            if file_path.stat().st_size > MAX_RST_BYTES:
                raise OSError('RST file exceeds the 2 MiB viewer limit')
            value = file_path.read_text(encoding='utf-8', errors='replace')
        except OSError as exc:
            self._display(self._msg('Nie można odczytać pliku: ', 'Cannot read file: ') + str(exc))
            return
        self._display(value, is_rst=True)

