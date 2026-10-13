"""Read-only, lazy browser of this installed pytracker-gui's *current* Markdown guides.

The allowlist excludes historical ADRs, development logs and other repositories.
No filesystem recursion, network access, subprocess, write-back, timers or threads.
"""
from pathlib import Path
import tkinter as tk
from tkinter import ttk

from .document_render import configure_document_tags, render_document
from .theme import COLORS

MAX_GUI_DOC_BYTES = 1024 * 1024

# Relative to the installed pytracker-gui project root; explicit list, never
# inferred from arbitrary input or a separate checkout / current working dir.
_CURRENT = (
    ('Project overview', 'README.md'),
    ('Windows / Git Bash', 'README_WINDOWS_GIT_BASH_{lang}.md'),
    ('User guide', 'docs/USER_GUIDE_{lang}.md'),
    ('Documentation index', 'docs/DOCUMENTATION_INDEX_{lang}.md'),
    ('Parameter manual', 'docs/PARAMETER_MANUAL_{lang}.md'),
)
_FEATURES = (
    ('GUI Settings reference', 'docs/GUI_SETTINGS_HELP_V032_{lang}.md'),
    ('Manual: upstream .rst', 'docs/MANUAL_UPSTREAM_RST_V026_{lang}.md'),
    ('Manual: demo instructions', 'docs/MANUAL_DEMO_TREE_V0210_{lang}.md'),
    ('Exact run/session binding', 'docs/SESSION_MEASUREMENT_BINDING_V028_{lang}.md'),
    ('Auto-show logs', 'docs/AUTO_LOG_DISPLAY_V029_{lang}.md'),
    ('Incremental console journal', 'docs/INCREMENTAL_SINGLE_LOG_V0212_{lang}.md'),
    ('Logs: history and settings', 'docs/LOGS_HISTORY_STAGE1_V0213_{lang}.md'),
    ('Logs: console viewer', 'docs/LOGS_CONSOLE_VIEWER_V0214_{lang}.md'),
    ('Classic buttons and movable panels', 'docs/CLASSIC_BUTTONS_RESIZABLE_PANELS_V0216_{lang}.md'),
    ('GUI documentation tab', 'docs/GUI_DOCUMENTATION_V0217_{lang}.md'),
)


def discover_gui_documents(project_root):
    """Return {language: {section: [(title, relative_path, absolute_path)]}}.

    Only regular non-symlinked files in this GUI install are listed. A missing
    documentation file is omitted rather than causing errors elsewhere.
    """
    root = Path(project_root).expanduser().resolve()
    if not root.is_dir() or (root / 'docs').is_symlink():
        return {}
    grouped = {}
    for language in ('en', 'pl'):
        sections = {}
        for section_name, records in (('current', _CURRENT), ('features', _FEATURES)):
            documents = []
            for title, template in records:
                relative = template.format(lang=language.upper())
                path = root / relative
                if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root):
                    continue
                documents.append((title, relative, path.resolve()))
            if documents:
                sections[section_name] = documents
        if sections:
            grouped[language] = sections
    return grouped


class GuiDocumentationBrowser(ttk.Frame):
    """Native Treeview: language -> current guides/features -> document."""

    def __init__(self, master, language='pl', project_root=None):
        super().__init__(master, padding=8)
        self.language = language
        self.project_root = (Path(project_root) if project_root is not None
                             else Path(__file__).resolve().parent.parent).resolve()
        self.groups = discover_gui_documents(self.project_root)
        self.node_paths = {}
        self.current_file = None

        self.status = ttk.Label(self, style='Muted.TLabel')
        self.status.pack(anchor='w', pady=(0, 8))
        panes = ttk.Panedwindow(self, orient='horizontal')
        panes.pack(fill='both', expand=True)
        left, right = ttk.Frame(panes), ttk.Frame(panes)
        panes.add(left, weight=1)
        panes.add(right, weight=3)
        style = ttk.Style(self)
        style.configure('GuiDocs.Treeview', background=COLORS['field'],
                        fieldbackground=COLORS['field'], foreground=COLORS['text'],
                        bordercolor=COLORS['border'], rowheight=27)
        style.map('GuiDocs.Treeview',
                  background=[('selected', COLORS['selection'])],
                  foreground=[('selected', COLORS['accent_text'])])
        self.tree = ttk.Treeview(left, show='tree', selectmode='browse', style='GuiDocs.Treeview')
        scrollbar = ttk.Scrollbar(left, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.tree.bind('<<TreeviewSelect>>', self._selected)
        self.text = tk.Text(right, wrap='word', state='disabled', relief='flat',
                            borderwidth=0, padx=16, pady=12,
                            background=COLORS['field'], foreground=COLORS['text'])
        text_scroll = ttk.Scrollbar(right, orient='vertical', command=self.text.yview)
        self.text.configure(yscrollcommand=text_scroll.set)
        self.text.pack(side='left', fill='both', expand=True)
        text_scroll.pack(side='right', fill='y')
        configure_document_tags(self.text)
        self._populate()
        self.set_language(language)
        self._empty()

    def _msg(self, pl, en):
        return en if self.language == 'en' else pl

    def _populate(self):
        self.tree.delete(*self.tree.get_children(''))
        self.node_paths.clear()
        for language, sections in self.groups.items():
            lang_node = self.tree.insert('', 'end', text='Polski' if language == 'pl' else 'English',
                                         open=(language == self.language))
            for section, documents in sections.items():
                label = ('Aktualne przewodniki' if language == 'pl' else 'Current guides') if section == 'current' else ('Dokumentacja funkcji' if language == 'pl' else 'Feature guides')
                group_node = self.tree.insert(lang_node, 'end', text=label, open=(section == 'current'))
                for title, relative, path in documents:
                    leaf = self.tree.insert(group_node, 'end', text=title)
                    self.node_paths[leaf] = (relative, path)

    def set_language(self, language):
        self.language = language
        self.status.configure(text=self._msg('Dokumentacja lokalnego pytracker-gui (tylko odczyt)',
                                             'Local pytracker-gui documentation (read-only)'))
        if self.current_file is None:
            self._empty()

    def _display(self, message):
        self.text.configure(state='normal')
        self.text.delete('1.0', 'end')
        self.text.insert('end', message)
        self.text.configure(state='disabled')
        self.text.yview_moveto(0)

    def _empty(self):
        self._display(self._msg('Wybierz dokument w drzewie po lewej.' if self.groups else
                                'Nie znaleziono dokumentacji bieżącej instalacji pytracker-gui.',
                                'Select a document from the tree on the left.' if self.groups else
                                'No documentation found in this pytracker-gui installation.'))

    def _selected(self, _event=None):
        selection = self.tree.selection()
        if not selection:
            return
        selected = self.node_paths.get(selection[0])
        if selected is None:
            return
        self.select_file(selected[0])

    def show_topic(self, key):
        """Locate a section by its literal GUI option key, without rescanning files."""
        marker = ("Opcja: " if self.current_file and self.current_file.endswith("_PL.md")
                  else "Option: ") + key
        position = self.text.search(marker, "1.0", stopindex="end", nocase=False)
        if position:
            self.text.see(position)

    def select_file(self, relative_path):
        """Read exactly one indexed local Markdown file, with revalidation."""
        selected = next((value for value in self.node_paths.values()
                         if value[0] == relative_path), None)
        if selected is None:
            raise KeyError(relative_path)
        relative, path = selected
        self.current_file = relative
        try:
            if path.is_symlink() or not path.resolve().is_relative_to(self.project_root):
                raise OSError('File outside installed GUI documentation')
            if path.stat().st_size > MAX_GUI_DOC_BYTES:
                raise OSError('Document exceeds the 1 MiB limit')
            content = path.read_text(encoding='utf-8', errors='replace')
        except OSError as error:
            self._display(self._msg('Nie można odczytać dokumentu: ',
                                    'Cannot read document: ') + str(error))
            return
        render_document(self.text, content, 'md')
