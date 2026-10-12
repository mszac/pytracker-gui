"""Lazy Logs history: project → run → settings or bounded console journal.

No watchers, background I/O, writes or PsychoPy imports.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .log_history import list_projects, list_runs, read_run
from .log_viewer import journal_for_run, read_page, tail_offset, preceding_offset, PAGE_BYTES
from .theme import COLORS, style_listbox

# Additional colors belong ONLY to this screen; the v0.2.6 global theme is frozen.
ACCENTS = {'technical': '#72addb', 'partial': '#e7b45a', 'complete': COLORS['success'],
           'selection': '#ffc187', 'selection_text': '#131820'}
TEXTS = {
    'pl': {
        'header':'Logi eksperymentów', 'sub':'Projekty i historia uruchomień · tylko do odczytu',
        'projects':'Projekty', 'runs':'Uruchomienia', 'refresh':'Odśwież',
        'empty':'Brak projektów z katalogiem experiments',
        'empty_runs':'Brak uruchomień w wybranym projekcie',
        'choose':'Wybierz projekt i uruchomienie z lewej strony.',
        'settings':'Ustawienia', 'console':'Log konsoli',
        'first':'Początek', 'previous':'Poprzedni', 'next':'Następny',
        'latest':'Ostatnie', 'reload':'Odśwież log', 'copy_page':'Kopiuj fragment',
        'no_log':'Brak dziennika dla tego uruchomienia.',
        'partial_note':'Niepełny dziennik (.log.part) — możliwe przerwanie lub utrata danych.',
        'complete_note':'Kompletny zapis dziennika; nie oznacza sukcesu eksperymentu.',
        'log_error':'Nie można odczytać dziennika:', 'page':'Bajty',
        'intro':'Wybrane uruchomienie', 'started':'Rozpoczęto', 'journal':'Dziennik',
        'ident':'Identyfikacja', 'environment':'Środowisko', 'execution':'Uruchomienie',
        'dataset':'Dane wejściowe', 'display':'Monitor i wygląd', 'configuration':'Konfiguracja',
        'show':'Pokaż szczegóły konfiguracji', 'hide':'Ukryj szczegóły konfiguracji',
        'error':'Nie można odczytać ustawień tego uruchomienia:',
        'incomplete':'NIEPEŁNY', 'complete':'KOMPLETNY', 'missing':'BRAK LOGU',
        'noresult':'Status procesu', 'preview':'Raport na podstawie kopii konfiguracji uruchomienia',
        'nodata':'Nie odnaleziono kopii YAML dla tego uruchomienia.',
    },
    'en': {
        'header':'Experiment logs', 'sub':'Project & run history · read-only',
        'projects':'Projects', 'runs':'Runs', 'refresh':'Refresh',
        'empty':'No projects with an experiments directory',
        'empty_runs':'No runs in the selected project',
        'choose':'Choose a project and run on the left.',
        'settings':'Settings', 'console':'Console Log',
        'first':'First', 'previous':'Previous', 'next':'Next',
        'latest':'Latest', 'reload':'Refresh log', 'copy_page':'Copy page',
        'no_log':'No journal available for this run.',
        'partial_note':'Incomplete journal (.log.part) — may have been interrupted or lost data.',
        'complete_note':'Journal is complete; this does not mean the experiment succeeded.',
        'log_error':'Could not read journal:', 'page':'Bytes',
        'intro':'Selected run', 'started':'Started', 'journal':'Journal',
        'ident':'Identification', 'environment':'Environment', 'execution':'Execution',
        'dataset':'Input data', 'display':'Display & appearance', 'configuration':'Configuration',
        'show':'Show additional settings', 'hide':'Hide additional settings',
        'error':'Could not read settings for this run:',
        'incomplete':'INCOMPLETE', 'complete':'COMPLETE', 'missing':'NO LOG',
        'noresult':'Process status', 'preview':'Report from the saved run configuration',
        'nodata':'No readable YAML snapshots found for this run.',
    },
}


def short(value, length=46):
    """One compact label line; full technical details remain expandable."""
    value = str(value).replace('\n', ' ').replace('\r', ' ')
    return value if len(value) <= length else value[:length-1] + '…'


class LogsHistoryScreen(ttk.Frame):
    """No ownership of experiment editor or runner; all filesystem access is on demand."""

    def __init__(self, master, projects_root, language='pl'):
        super().__init__(master, padding=(15, 12))
        self.projects_root = projects_root
        self.language = language if language in TEXTS else 'pl'
        self.projects = []
        self.runs = []
        self.selected_project = None
        self.selected_run = None
        self.report = None
        self._reported_key = None
        self._expanded = False
        self._view = 'settings'
        self._journal_path = None
        self._page_offset = 0
        self._page_history = []
        self._page_text = ''
        self._build()
        self._first_show = True
        self.refresh()

    def tr(self, key):
        return TEXTS[self.language][key]

    def _label(self, parent, value, *, color=None, size=11, bold=False, bg=None, **kw):
        return tk.Label(parent, text=value, font=('Segoe UI', size, 'bold' if bold else 'normal'),
                        bg=bg or COLORS['surface'], fg=color or COLORS['text'],
                        anchor='w', **kw)

    def _build(self):
        header = ttk.Frame(self)
        header.pack(fill='x', pady=(0, 10))
        self._setup_local_styles()
        self.title_label = ttk.Label(header, text=self.tr('header'), style='LogsTitle.TLabel')
        self.title_label.pack(anchor='w')
        self.subtitle_label = ttk.Label(header, text=self.tr('sub'), style='LogsMuted.TLabel')
        self.subtitle_label.pack(anchor='w', pady=(3, 0))
        ttk.Separator(self).pack(fill='x', pady=(0, 10))
        # Native, bounded separators; no resize polling, persistence or threads.
        self.logs_panels = tk.PanedWindow(
            self, orient='horizontal', bg=COLORS['border'], sashwidth=7,
            sashrelief='flat', bd=0, relief='flat', opaqueresize=True)
        self.logs_panels.pack(fill='both', expand=True)
        side = ttk.Frame(self.logs_panels, padding=(0, 0, 7, 0))
        self.logs_panels.add(side, minsize=228, stretch='never')
        self.project_run_panels = tk.PanedWindow(
            side, orient='vertical', bg=COLORS['border'], sashwidth=7,
            sashrelief='flat', bd=0, relief='flat', opaqueresize=True)
        self.project_run_panels.pack(fill='both', expand=True)
        projects_area = ttk.Frame(self.project_run_panels)
        runs_area = ttk.Frame(self.project_run_panels)
        self.project_run_panels.add(projects_area, minsize=120, stretch='never')
        self.project_run_panels.add(runs_area, minsize=140, stretch='always')
        bar = ttk.Frame(projects_area)
        bar.pack(fill='x', pady=(0, 5))
        self.projects_title = ttk.Label(bar, text=self.tr('projects'), style='LogsHeading.TLabel')
        self.projects_title.pack(side='left')
        self.refresh_btn = ttk.Button(bar, text=self.tr('refresh'), style='Logs.TButton', command=self.refresh)
        self.refresh_btn.pack(side='right')
        projects_box = ttk.Frame(projects_area)
        projects_box.pack(fill='both', expand=True)
        self.project_list = tk.Listbox(projects_box, height=6, exportselection=False,
                                       font=('TkDefaultFont', 11), selectmode='browse', takefocus=True)
        style_listbox(self.project_list)
        self._style_local_list(self.project_list)
        self.project_list.pack(fill='both', expand=True)
        self.run_title = ttk.Label(runs_area, text=self.tr('runs'), style='LogsHeading.TLabel')
        self.run_title.pack(anchor='w', pady=(0, 5))
        runs_box = ttk.Frame(runs_area)
        runs_box.pack(fill='both', expand=True)
        self.run_list = tk.Listbox(runs_box, exportselection=False, font=('TkDefaultFont', 11),
                                  selectmode='browse', takefocus=True)
        style_listbox(self.run_list)
        self._style_local_list(self.run_list)
        self.run_list.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(runs_box, orient='vertical', command=self.run_list.yview)
        scrollbar.pack(side='right', fill='y')
        self.run_list.configure(yscrollcommand=scrollbar.set)
        self.project_list.bind('<<ListboxSelect>>', self._choose_project)
        self.run_list.bind('<<ListboxSelect>>', self._choose_run)

        self.content = ttk.Frame(self.logs_panels, padding=(7, 0, 0, 0))
        self.logs_panels.add(self.content, minsize=390, stretch='always')
        self.details = ttk.Frame(self.content)
        self.details.pack(fill='both', expand=True)
        self.empty_label = ttk.Label(self.details, style='LogsMuted.TLabel', text=self.tr('choose'))
        self.empty_label.pack(anchor='center', pady=45)

    def _setup_local_styles(self):
        style = ttk.Style(self)
        style.configure('LogsTitle.TLabel', background=COLORS['surface'], foreground=COLORS['text'],
                        font=('TkDefaultFont', 17, 'bold'))
        style.configure('LogsHeading.TLabel', background=COLORS['surface'], foreground=COLORS['text'],
                        font=('TkDefaultFont', 12, 'bold'))
        style.configure('LogsMuted.TLabel', background=COLORS['surface'], foreground=COLORS['muted'],
                        font=('TkDefaultFont', 11))
        style.configure('Logs.TButton', font=('TkDefaultFont', 11))
        style.configure('LogsAccent.TButton', font=('TkDefaultFont', 11, 'bold'),
                        background=COLORS['accent'], foreground=COLORS['accent_text'])
        style.map('LogsAccent.TButton', foreground=[('active', COLORS['accent_text'])],
                  background=[('active', COLORS['accent_hover'])])

    @staticmethod
    def _style_local_list(widget):
        # Local highlight: significantly lighter than global selection #ff8931.
        widget.configure(selectbackground=ACCENTS['selection'],
                         selectforeground=ACCENTS['selection_text'])

    def _reset_journal(self):
        self._journal_path = None
        self._page_offset = 0
        self._page_history = []
        self._page_text = ''

    def set_language(self, language):
        self.language = language if language in TEXTS else 'pl'
        self.title_label.configure(text=self.tr('header'))
        self.subtitle_label.configure(text=self.tr('sub'))
        self.projects_title.configure(text=self.tr('projects'))
        self.run_title.configure(text=self.tr('runs'))
        self.refresh_btn.configure(text=self.tr('refresh'))
        self._render()

    def on_show(self):
        """Refresh on entry only (or via button), never by timer or observer."""
        if self._first_show:
            self._first_show = False
        else:
            self.refresh()

    def refresh(self):
        self._reported_key = None  # explicit refresh reloads selected snapshots
        self._reset_journal()
        prior_project = self.selected_project.name if self.selected_project else None
        prior_run = self.selected_run.name if self.selected_run else None
        self.projects = list_projects(self.projects_root)
        self.project_list.delete(0, 'end')
        for item in self.projects:
            self.project_list.insert('end', f'▸ {item.name}   ({item.run_count})')
        index = next((i for i, p in enumerate(self.projects) if p.name == prior_project), 0)
        if self.projects:
            self.project_list.selection_set(index)
            self.project_list.activate(index)
            self._set_project(self.projects[index], prior_run)
        else:
            self.selected_project = None
            self.selected_run = None
            self.runs = []
            self.run_list.delete(0, 'end')
            self._render()

    def _choose_project(self, _event):
        indexes = self.project_list.curselection()
        if indexes and indexes[0] < len(self.projects):
            self._set_project(self.projects[indexes[0]], None)

    def _set_project(self, project, prior_run):
        self.selected_project = project
        self.runs = list_runs(project.directory)
        self.run_list.delete(0, 'end')
        for index, item in enumerate(self.runs):
            marker = {'complete': '●', 'partial': '◐', 'none': '○'}[item.journal]
            self.run_list.insert('end', f'{marker}  {item.timestamp[:8]} {item.timestamp[9:]}   {item.run_id}')
            self.run_list.itemconfig(index, foreground={
                'complete': ACCENTS['complete'], 'partial': ACCENTS['partial'],
                'none': COLORS['muted']}[item.journal])
        index = next((i for i, r in enumerate(self.runs) if r.name == prior_run), 0)
        if self.runs:
            self.run_list.selection_set(index)
            self.run_list.activate(index)
            self.selected_run = self.runs[index]
        else:
            self.selected_run = None
        self._expanded = False
        self._view = 'settings'
        self._reset_journal()
        self._render()

    def _choose_run(self, _event):
        indexes = self.run_list.curselection()
        if indexes and indexes[0] < len(self.runs):
            self.selected_run = self.runs[indexes[0]]
            self._expanded = False
            self._render()

    def _wipe(self):
        for child in self.details.winfo_children():
            child.destroy()

    def _render(self):
        self._wipe()
        if not self.selected_project:
            self._label(self.details, self.tr('empty'), color=COLORS['muted']).pack(anchor='w', pady=25)
            return
        if not self.selected_run:
            self._label(self.details, self.tr('empty_runs'), color=COLORS['muted']).pack(anchor='w', pady=25)
            return
        try:
            key = (self.selected_project.name, self.selected_run.name)
            if self._reported_key != key:
                self.report = read_run(self.selected_run, self.selected_project)
                self._reported_key = key
        except (OSError, ValueError, UnicodeError, TypeError) as exc:
            self.report = None
            self._reported_key = None
            self._label(self.details, self.tr('error'), color=ACCENTS['partial'], bold=True).pack(anchor='w', pady=(12, 5))
            self._label(self.details, short(str(exc), 110), color=COLORS['muted'], wraplength=540).pack(anchor='w')
            return
        d = self.report
        top = tk.Frame(self.details, bg=COLORS['surface_alt'], padx=13, pady=10)
        top.pack(fill='x', pady=(0, 9))
        self._label(top, self.tr('intro') + '   ·   ' + d['project'], bg=COLORS['surface_alt'],
                    color=COLORS['muted'], size=10).pack(anchor='w')
        status_label = {'complete': self.tr('complete'), 'partial': self.tr('incomplete'),
                        'none': self.tr('missing')}[d['journal']]
        status_color = {'complete': ACCENTS['complete'], 'partial': ACCENTS['partial'],
                        'none': COLORS['muted']}[d['journal']]
        line = tk.Frame(top, bg=COLORS['surface_alt'])
        line.pack(fill='x', pady=(3, 2))
        self._label(line, 'RUN ' + d['run_id'], bg=COLORS['surface_alt'], bold=True, size=15).pack(side='left')
        self._label(line, status_label, bg=COLORS['surface_alt'], size=10,
                    color=status_color, bold=True).pack(side='right')
        self._label(top, f'{d["started"][:8]}  {d["started"][9:]}   ·   {short(d["process_status"], 65)}',
                    bg=COLORS['surface_alt'], color=COLORS['muted'], size=10).pack(anchor='w')

        tabs = ttk.Frame(self.details)
        tabs.pack(fill='x', pady=(0, 8))
        self.settings_btn = ttk.Button(tabs, text=self.tr('settings'),
                                       style='LogsAccent.TButton' if self._view == 'settings' else 'Logs.TButton',
                                       command=lambda: self._set_view('settings'))
        self.settings_btn.pack(side='left')
        self.console_btn = ttk.Button(tabs, text=self.tr('console'),
                                      style='LogsAccent.TButton' if self._view == 'console' else 'Logs.TButton',
                                      command=lambda: self._set_view('console'))
        self.console_btn.pack(side='left', padx=(9, 0))

        if self._view == 'console':
            self._render_console()
            return

        cards = ttk.Frame(self.details)
        cards.pack(fill='x')
        cards.columnconfigure(0, weight=1, uniform='logs')
        cards.columnconfigure(1, weight=1, uniform='logs')
        sections = (
            ('ident', [('Project', d['project']), ('Variant', d['variant']), ('Run', d['run_id'])], COLORS['accent']),
            ('environment', [('Gaze', d['gaze']), ('Python', d['python']), ('ioHub', d['eye'])], ACCENTS['technical']),
            ('execution', [('Blocks / trials', d['trials']), ('Voice / raw', f'{d["voice"]} / {d["raw_data"]}'),
                            ('Log level', d['log_level'])], COLORS['accent']),
            ('dataset', [('Input', d['data']), ('Blocks', d['blocks'])], ACCENTS['technical']),
            ('display', [('Monitor', d['monitor']), ('Resolution', d['resolution']),
                         ('Button / font', f'{d["button_size"]} / {d["font_size"]}')], COLORS['accent']),
            ('configuration', [('Snapshots', d['snapshots']), ('ioHub', d['eye'])], ACCENTS['technical']),
        )
        for i, (title, items, accent) in enumerate(sections):
            card = tk.Frame(cards, bg=COLORS['surface_alt'], highlightthickness=1,
                            highlightbackground=COLORS['border'], padx=11, pady=8)
            card.grid(row=i//2, column=i%2, sticky='nsew', padx=(0, 7) if i%2==0 else (7, 0), pady=(0, 9))
            self._label(card, self.tr(title), size=11, bold=True,
                        color=accent, bg=COLORS['surface_alt']).pack(anchor='w', pady=(0, 5))
            for key, val in items:
                self._label(card, f'{key}:  {short(val, 42)}', bg=COLORS['surface_alt'],
                            size=10).pack(anchor='w', pady=1)
        self.more_button = ttk.Button(self.details, text=self.tr('hide') if self._expanded else self.tr('show'),
                                       style='Logs.TButton', command=self._toggle_details)
        self.more_button.pack(anchor='w', pady=(0, 5))
        if self._expanded:
            self._show_details(d)
        self._label(self.details, self.tr('preview'), size=9, color=COLORS['muted']).pack(anchor='w', pady=(4, 0))

    def _toggle_details(self):
        self._expanded = not self._expanded
        self._render()

    def _show_details(self, d):
        box = tk.Frame(self.details, bg=COLORS['field'], padx=8, pady=5)
        box.pack(fill='both', expand=True, pady=(0, 4))
        lines = []
        for filename, groups in d['yaml_details']:
            lines.append('[' + filename + ']')
            for heading, entries in groups.items():
                if entries:
                    lines.append('  ' + heading)
                    lines.extend(f'    {k}: {value}' for k, value in entries)
        if d['yaml_errors']:
            lines.append('NOTE: ' + d['yaml_errors'])
        if not lines:
            lines.append(self.tr('nodata'))
        text = tk.Text(box, height=7, wrap='word', bg=COLORS['field'], fg=COLORS['text'],
                       insertbackground=COLORS['text'], relief='flat', font=('TkFixedFont', 10),
                       padx=4, pady=3, selectbackground=COLORS['selection'],
                       selectforeground=COLORS['accent_text'])
        text.pack(side='left', fill='both', expand=True)
        scroll = ttk.Scrollbar(box, command=text.yview)
        scroll.pack(side='right', fill='y')
        text.configure(yscrollcommand=scroll.set)
        text.insert('1.0', '\n'.join(lines))
        text.configure(state='disabled')

    def _set_view(self, view):
        if view not in ('settings', 'console') or view == self._view:
            return
        self._view = view
        if view == 'console':
            self._reset_journal()
        self._render()

    def _load_page(self, offset=0, *, remember=True):
        if self._journal_path is None:
            return
        if remember and offset != self._page_offset:
            self._page_history.append(self._page_offset)
        self._page_offset = offset
        self._render_console_page()

    def _previous_page(self):
        if self._page_history:
            self._page_offset = self._page_history.pop()
        elif self._journal_path and self._page_offset:
            self._page_offset = preceding_offset(self._journal_path, self._page_offset)
        self._render_console_page()

    def _refresh_console(self):
        # Manual refresh, including a growing .part; never schedule polling.
        self._reset_journal()
        self._render_console_page()

    def _copy_page(self):
        self.clipboard_clear()
        self.clipboard_append(self._page_text)

    def _render_console(self):
        self._label(self.details, self.tr('partial_note') if self.selected_run.journal == 'partial'
                    else self.tr('complete_note') if self.selected_run.journal == 'complete'
                    else self.tr('no_log'), color=(ACCENTS['partial'] if self.selected_run.journal == 'partial'
                    else COLORS['muted']), size=10, wraplength=760).pack(anchor='w', pady=(0, 8))
        toolbar = ttk.Frame(self.details)
        toolbar.pack(fill='x', pady=(0, 7))
        nav_buttons = ttk.Frame(toolbar)
        nav_buttons.pack(fill='x')
        extra_buttons = ttk.Frame(toolbar)
        extra_buttons.pack(fill='x', pady=(3, 0))
        self.console_actions = {}
        for name, callback in (
            ('first', lambda: self._load_page(0)),
            ('previous', self._previous_page),
            ('next', self._next_page),
            ('latest', self._latest_page),
            ('reload', self._refresh_console),
            ('copy_page', self._copy_page),
        ):
            button = ttk.Button(nav_buttons if name in ('first', 'previous', 'next', 'latest')
                                else extra_buttons, text=self.tr(name), style='Logs.TButton',
                                command=callback)
            button.pack(side='left', padx=(0, 4))
            self.console_actions[name] = button
        panel = ttk.Frame(self.details)
        panel.pack(fill='both', expand=True)
        panel.rowconfigure(0, weight=1)
        panel.columnconfigure(0, weight=1)
        self.console_text = tk.Text(panel, wrap='none', height=16,
                                    bg=COLORS['field'], fg=COLORS['text'],
                                    selectbackground=ACCENTS['selection'],
                                    selectforeground=ACCENTS['selection_text'],
                                    font=('TkFixedFont', 11), relief='flat',
                                    padx=9, pady=7, state='disabled')
        self.console_text.grid(row=0, column=0, sticky='nsew')
        scroll_y = ttk.Scrollbar(panel, orient='vertical', command=self.console_text.yview)
        scroll_y.grid(row=0, column=1, sticky='ns')
        scroll_x = ttk.Scrollbar(panel, orient='horizontal', command=self.console_text.xview)
        scroll_x.grid(row=1, column=0, sticky='ew')
        self.console_text.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.console_position = self._label(self.details, '', size=10, color=COLORS['muted'])
        self.console_position.pack(anchor='w', pady=(5, 0))
        self._render_console_page()

    def _render_console_page(self):
        # Re-render only this bounded page; do not reconstruct the cards or tab.
        if not hasattr(self, 'console_text') or not self.console_text.winfo_exists():
            return
        try:
            path, integrity = journal_for_run(self.selected_run)
            if path is None:
                self._journal_path = None
                text, begin, end, size = self.tr('no_log'), 0, 0, 0
            else:
                if self._journal_path != path:
                    self._journal_path = path
                    self._page_offset = 0
                    self._page_history = []
                text, begin, end, size = read_page(path, self._page_offset)
                self._page_offset = begin
        except (OSError, ValueError, UnicodeError) as exc:
            self._journal_path = None
            text, begin, end, size = self.tr('log_error') + ' ' + short(exc, 160), 0, 0, 0
        self._page_text = text
        self._page_end = end
        self._page_size = size
        self.console_text.configure(state='normal')
        self.console_text.delete('1.0', 'end')
        self.console_text.insert('1.0', text)
        self.console_text.configure(state='disabled')
        self.console_position.configure(text=(f'{self.tr("page")}: {begin:,}–{end:,} / {size:,}'
                                              f'  ·  max {PAGE_BYTES // 1024} KiB/page'))
        for name, enabled in (
            ('first', bool(self._journal_path and begin)),
            ('previous', bool(self._journal_path and begin)),
            ('next', bool(self._journal_path and end < size)),
            ('latest', bool(self._journal_path)),
            ('reload', True),
            ('copy_page', bool(text and self._journal_path)),
        ):
            self.console_actions[name].state(['!disabled'] if enabled else ['disabled'])

    def _next_page(self):
        if self._journal_path is not None and self._page_end < self._page_size:
            self._load_page(self._page_end)

    def _latest_page(self):
        if self._journal_path is not None:
            try:
                offset = tail_offset(self._journal_path)
            except (OSError, ValueError):
                self._render_console_page()
                return
            self._load_page(offset)
