"""Tkinter project configuration editor and native experiment launcher."""
import json
import os
import shutil
import sys
import tempfile
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from tkinter.scrolledtext import ScrolledText
from . import __version__
from .catalog import CATALOG
from .layout import choose_roots, canonical_roots, default_eye_config, validate_layout
from .environment import probe_interpreter
from .fields import DATASET_FIELDS, MONITOR_FIELDS, APPEARANCE_FIELDS, active_fields, parse_field, to_text
from .profiles import ProfileStore
from .projects import ProjectStore, ProjectError
from .storage import atomic_write
from .storage import data_home, load_settings, save_settings
from .validation import validate_config, check_demo_root, Finding
from .yamlconfig import load_text, dump_doc, read_source, update_value, get_value
from .help_widgets import InfoButton, InfoPopover
from .parameter_help import get_parameter_help
from .i18n import translate
from .runtime import prepare_run, LaunchError
from .runner import ExperimentRunner
from .theme import apply_theme, COLORS, icon, set_icon, style_listbox, style_text


TABS = ('Dane', 'Monitor', 'Wygląd', 'Instrukcje', 'YAML', 'Uruchomienie')
GROUPS = {'Dane':DATASET_FIELDS,'Monitor':MONITOR_FIELDS,'Wygląd':APPEARANCE_FIELDS}
# Only inactive icons within Experiment; orange selected and ink-on-accent remain unchanged.
EXPERIMENT_DEFAULT_ICON_COLOR = '#A46628'


def _enable_hidpi_awareness():
    """Best-effort native HiDPI support for crisper Windows text and icons.

    This is intentionally lightweight: no new dependencies, no background work,
    and safe fallbacks on older Windows versions or non-Windows platforms.
    """
    if sys.platform != 'win32':
        return
    try:
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # per-monitor aware
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        return


def _configure_tk_scaling(root):
    """Use the real monitor DPI for sharper Tk rendering when available."""
    try:
        dpi = float(root.winfo_fpixels('1i'))
        if dpi > 0:
            root.tk.call('tk', 'scaling', dpi / 72.0)
    except Exception:
        pass


class PytrackerGUI(ttk.Frame):
    def __init__(self, master, *, home=None, on_language_change=None):
        super().__init__(master, padding=12)
        self.root = self.winfo_toplevel()
        self.on_language_change = on_language_change
        self.on_manual_request = None
        self.home = Path(home) if home is not None else data_home()
        # Projects are independent of the GUI checkout and of source/demo code.
        # An explicitly injected home isolates automated tests from live projects.
        self.project_root = ((self.home / 'projects') if home is not None else
                             Path(choose_roots(load_settings(self.home))[0]) / 'projects')
        self.projects = ProjectStore(self.project_root)
        self._active_project = None
        self._active_project_demo = None
        self.store = ProfileStore(self.home)
        self._active_manifest = None
        self.runner = ExperimentRunner()
        self.run_console = None
        self.run_log = None
        self._run_display_lines = []  # bounded, recent preview only
        self._run_preview_chars = 0
        self._run_preview_lines = 0
        self._run_spool = None  # complete ordered GUI log; spills to OS temp above 256 KiB
        self._run_spool_failed = False
        self._last_experiment_log = None
        self._run_poll_id = None
        self.settings = load_settings(self.home)
        self.demo = None
        self.active_block_key = None
        self.docs = {}
        self.hashes = {}
        self.loaded = False
        self.loop_by_block = {}
        self.persisted_prefs = None
        self.dirty = False
        self.raw_dirty = False
        self._block_update = False
        self._tab_update = False
        self.info_popover = InfoPopover(self.root, lambda key: get_parameter_help(key, self.help_language_code),
                                        on_manual=self._open_manual_for)
        # Ordinary clicks outside an info button dismiss the bubble.
        # InfoButton's own click binding returns 'break', so it is not closed immediately.
        self.root.bind('<Button-1>', lambda _event: self.info_popover.dismiss(), add='+')
        self.root.bind('<Escape>', lambda _event: self.info_popover.dismiss(), add='+')
        self.bind('<Destroy>', self._log_view_destroyed, add='+')
        self.field_vars = {}
        self.active_tab = 'Dane'
        self._make_vars()
        self._styles()
        self._make_layout()
        self.pack(fill='both', expand=True)
        self._select_demo(0, ask=False)
        self._apply_language()


    def _open_manual_for(self, key):
        if self.on_manual_request is not None:
            self.on_manual_request(key)

    def _make_vars(self):
        upstream_root, demo_root = choose_roots(self.settings)
        self.demo_root = tk.StringVar(value=str(demo_root))
        self.upstream = tk.StringVar(value=str(upstream_root))
        self.python = tk.StringVar(value=self.settings.get('python', sys.executable))
        self.gaze = tk.StringVar(value='mouse')
        self.eye = tk.StringVar(value='')
        self.voice = tk.BooleanVar(value=False)
        self.raw_data = tk.BooleanVar(value=False)
        self.loop = tk.StringVar(value='3')
        self.log_level = tk.StringVar(value='info')
        self.auto_show_logs = tk.BooleanVar(value=self.settings.get('auto_show_logs', True) is not False)
        self.status = tk.StringVar(value='Automatyczny układ: tobii-pytracker/{tobii-pytracker-demo,pytracker-gui}. Uruchamianie projektów dostępne w zakładce Uruchomienie.')
        self.block_name = tk.StringVar()
        self.project_name = tk.StringVar()
        self.language_code = self.settings.get('language', 'pl')
        if self.language_code not in ('pl', 'en'):
            self.language_code = 'pl'
        self.help_language_code = self.settings.get('help_language', self.language_code)
        if self.help_language_code not in ('pl', 'en'):
            self.help_language_code = 'pl'
        self.language_name = tk.StringVar(value='Polski' if self.language_code == 'pl' else 'English')
        self.help_language_name = tk.StringVar(value='Polski' if self.help_language_code == 'pl' else 'English')
        self.help_language_explicit = bool(self.settings.get('help_language_explicit', False))
        self.status.set(self._t(self.status.get()))

    def _styles(self):
        # Single native ttk palette, installed once for both standalone and shell use.
        # Presentation only: no additional timers, threads or processing.
        apply_theme(self.root)

    def _experiment_icon(self, name, active=False):
        # An explicit GUI Settings icon preference takes precedence over this
        # Experiment-only default. Active/ink states use packaged PNGs unchanged.
        color = None if self.settings.get('ICON_COLOR') else EXPERIMENT_DEFAULT_ICON_COLOR
        return icon(self.root, name, active=active, color=color)

    def _set_experiment_icon(self, widget, name, active=False):
        widget.configure(image=self._experiment_icon(name, active), compound='left')

    def _t(self, text):
        return translate(text, self.language_code)

    @staticmethod
    def _language_value(value):
        return 'en' if value == 'English' else 'pl'

    def _store_language_preferences(self):
        # Add UI-only preferences to the existing settings without resetting paths.
        self.settings.update({'language': self.language_code, 'help_language': self.help_language_code,
                              'help_language_explicit': self.help_language_explicit})
        save_settings(self.home, self.settings)

    def _translate_widgets(self, widget):
        """Refresh only text properties, never destroy controls or edit field values."""
        if widget not in (self.demo_label, self.desc_label, self.gaze_help):
            try:
                source = getattr(widget, '_ui_source_text', None)
                if source is None:
                    source = widget.cget('text')
                    widget._ui_source_text = source
                if source:
                    widget.configure(text=self._t(source))
            except (tk.TclError, AttributeError):
                pass
        for child in widget.winfo_children():
            self._translate_widgets(child)

    def _apply_language(self):
        self.info_popover.dismiss()
        self._translate_widgets(self)
        for tab in TABS:
            self.tabs.tab(self.pages[tab], text=self._t(tab))
        if self.demo is not None:
            self.desc_label.configure(text=f'{self._t(self.demo.description)}  |  '
                f'{self._t("modalność: ")}{self.demo.modality}  |  '
                f'{self._t("backend: ")}{self.demo.engine}')
        self.demo_label.configure(text='Konfiguracja eksperymentu' if self.language_code == 'pl' else 'Experiment setup')
        self._gaze_changed()
        self._refresh_all()
        if self.on_language_change is not None:
            self.on_language_change()

    def _on_language_changed(self, _event=None):
        chosen = self._language_value(self.language_name.get())
        if chosen == self.language_code:
            return
        # Commit the active edit before rebuilding the tab; invalid YAML cancels
        # the language switch rather than losing unsaved user data.
        if not self._commit_tab():
            self.language_name.set('Polski' if self.language_code == 'pl' else 'English')
            return
        self.language_code = chosen
        old_help_code = self.help_language_code
        if not self.help_language_explicit:
            self.help_language_code = chosen
            self.help_language_name.set('Polski' if chosen == 'pl' else 'English')
        try:
            self._store_language_preferences()
        except OSError as exc:
            self.language_code = 'pl' if chosen == 'en' else 'en'
            self.language_name.set('Polski' if self.language_code == 'pl' else 'English')
            self.help_language_code = old_help_code
            self.help_language_name.set('Polski' if old_help_code == 'pl' else 'English')
            messagebox.showerror(self._t('Błąd zapisu'), str(exc), parent=self.root)
            return
        self._apply_language()
        self.status.set(self._t('Automatyczny układ: tobii-pytracker/{tobii-pytracker-demo,pytracker-gui}. Uruchamianie projektów dostępne w zakładce Uruchomienie.'))

    def _on_help_language_changed(self, _event=None):
        chosen = self._language_value(self.help_language_name.get())
        if chosen == self.help_language_code:
            return
        previous = self.help_language_code
        self.help_language_code = chosen
        previous_explicit = self.help_language_explicit
        self.help_language_explicit = True
        try:
            self._store_language_preferences()
        except OSError as exc:
            self.help_language_code = previous
            self.help_language_explicit = previous_explicit
            self.help_language_name.set('Polski' if previous == 'pl' else 'English')
            messagebox.showerror(self._t('Błąd zapisu'), str(exc), parent=self.root)
            return
        self.info_popover.dismiss()
        if self.on_language_change is not None:
            self.on_language_change()

    def _info_icon(self, parent, key):
        # Validate the key when creating the control, not only after user clicks.
        get_parameter_help(key)
        return InfoButton(parent, help_key=key, callback=self.info_popover.toggle)

    def _info_label(self, parent, label, key, *, width=None, style=None):
        group = ttk.Frame(parent)
        kwargs = {'text': label}
        if width is not None: kwargs['width'] = width
        if style is not None: kwargs['style'] = style
        ttk.Label(group, **kwargs).pack(side='left', anchor='center')
        self._info_icon(group, key).pack(side='left', padx=(5, 0))
        return group

    def _make_layout(self):
        self.root.title('pytracker-gui  •  M1  •  '+__version__)
        self.root.geometry('1190x830')
        self.root.minsize(940, 650)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.columnconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)

        title = ttk.Frame(self)
        title.grid(row=0,column=0,columnspan=2,sticky='ew',pady=(0,10))
        ttk.Label(title,text='pytracker-gui',style='Title.TLabel').pack(side='left')
        ttk.Label(title,text='M1 · konfiguracja i uruchamianie projektów',style='Muted.TLabel').pack(side='left',padx=18)
        ttk.Button(title,text='O projekcie',command=self._about).pack(side='right')
        languages=ttk.Frame(title)
        languages.pack(side='right',padx=(8,12))
        ttk.Label(languages,text='Język interfejsu').grid(row=0,column=0,sticky='e',padx=(0,4))
        self.language_combo=ttk.Combobox(languages,textvariable=self.language_name,
                                        values=('Polski','English'),state='readonly',width=9)
        self.language_combo.grid(row=0,column=1,padx=(0,12))
        self.language_combo.bind('<<ComboboxSelected>>',self._on_language_changed)
        ttk.Label(languages,text='Język podpowiedzi').grid(row=0,column=2,sticky='e',padx=(0,4))
        self.help_language_combo=ttk.Combobox(languages,textvariable=self.help_language_name,
                                             values=('Polski','English'),state='readonly',width=9)
        self.help_language_combo.grid(row=0,column=3)
        self.help_language_combo.bind('<<ComboboxSelected>>',self._on_help_language_changed)
        ttk.Label(languages,text='Manuale PL/EN: docs/PARAMETER_MANUAL_PL.md i docs/PARAMETER_MANUAL_EN.md',
                  style='Muted.TLabel').grid(row=1,column=0,columnspan=4,sticky='e',pady=(3,0))


        env=ttk.LabelFrame(self,text='Środowisko i repozytoria',padding=8)
        env.grid(row=1,column=0,columnspan=2,sticky='ew',pady=(0,10))
        env.columnconfigure(1,weight=1)
        for row,(label,var,kind) in enumerate((
            ('Katalog projektów startowych',self.demo_root,'dir'), ('Upstream',self.upstream,'dir'), ('Python 3.10',self.python,'file'))):
            help_key = ('gui.demo_root','gui.upstream_root','gui.python')[row]
            self._info_label(env,label,help_key,width=15).grid(row=row,column=0,sticky='w',pady=2)
            ttk.Entry(env,textvariable=var).grid(row=row,column=1,sticky='ew',padx=6,pady=2)
            ttk.Button(env,text='Wybierz…',command=lambda v=var,k=kind:self._browse(v,k)).grid(row=row,column=2,padx=3)
        save_paths_button=ttk.Button(env,text='Zapisz ścieżki',command=self._save_paths)
        save_paths_button.grid(row=0,column=3,padx=6,sticky='ew')
        self._set_experiment_icon(save_paths_button, 'save-environment')
        check_python_button=ttk.Button(env,text='Sprawdź Python',command=self._probe)
        check_python_button.grid(row=1,column=3,padx=6,sticky='ew')
        self._set_compact_icon(check_python_button, 'diagnostics')
        read_repo_button=ttk.Button(env,text='Wczytaj repo',command=self._reload)
        read_repo_button.grid(row=2,column=3,padx=6,sticky='ew')
        self._set_experiment_icon(read_repo_button, 'folder')
        detect_layout_button=ttk.Button(env,text='Wykryj układ',command=self._autodetect)
        detect_layout_button.grid(row=3,column=3,padx=6,pady=2,sticky='ew')
        self._set_experiment_icon(detect_layout_button, 'folder')
        ttk.Label(env,text='Układ wymagany przez run_native.sh: tobii-pytracker / tobii-pytracker-demo + pytracker-gui',
                  style='Muted.TLabel').grid(row=3,column=0,columnspan=3,sticky='w',pady=(3,0))

        # Native sash; only the panel boundary is movable. Original v0.2.14
        # buttons, fonts, arrangement and styles are intentionally unchanged.
        self.experiment_panels = tk.PanedWindow(
            self, orient='horizontal', bg=COLORS['border'], sashwidth=7,
            sashrelief='flat', bd=0, relief='flat', opaqueresize=True)
        self.experiment_panels.grid(row=2,column=0,columnspan=2,sticky='nsew')
        sidebar=ttk.LabelFrame(self.experiment_panels,text='Projekty startowe (7)',padding=9)
        self.experiment_panels.add(sidebar,minsize=220,stretch='never')
        sidebar.columnconfigure(0,weight=1)
        sidebar.rowconfigure(1,weight=1)
        self._info_label(sidebar,'Wybierz projekt startowy','gui.variant',style='Muted.TLabel').grid(row=0,column=0,sticky='w',pady=(0,7))
        listarea=ttk.Frame(sidebar)
        listarea.grid(row=1,column=0,sticky='nsew')
        listarea.columnconfigure(0,weight=1)
        listarea.rowconfigure(0,weight=1)
        scroll=ttk.Scrollbar(listarea,orient='vertical')
        scroll.grid(row=0,column=1,sticky='ns')
        self.listbox=tk.Listbox(listarea,selectmode=tk.SINGLE,exportselection=False,width=27,
                                height=7,activestyle='dotbox',font=('TkDefaultFont',10),
                                yscrollcommand=scroll.set)
        style_listbox(self.listbox)
        self.listbox.grid(row=0,column=0,sticky='nsew')
        scroll.configure(command=self.listbox.yview)
        for demo in CATALOG:
            self.listbox.insert('end',f'{demo.label}  [{demo.variant}]')
        self.listbox.bind('<<ListboxSelect>>',self._list_select)
        ttk.Separator(sidebar).grid(row=2,column=0,sticky='ew',pady=11)
        self._info_label(sidebar,'Źródło gaze','gui.gaze',style='Heading.TLabel').grid(row=3,column=0,sticky='w')
        for j,(name,value) in enumerate((('Brak rejestrowania','none'),('MouseGaze (mysz)','mouse'),('Tobii (urządzenie)','tobii'))):
            ttk.Radiobutton(sidebar,text=name,variable=self.gaze,value=value,command=self._gaze_changed).grid(row=4+j,column=0,sticky='w',pady=2)
        self._info_label(sidebar,'ioHub YAML (wybór ścieżki)','gui.iohub_yaml',style='Muted.TLabel').grid(row=7,column=0,sticky='w',pady=(9,3))
        ttk.Entry(sidebar,textvariable=self.eye,width=24).grid(row=8,column=0,sticky='ew')
        ttk.Button(sidebar,text='Wybierz plik ioHub…',command=lambda:self._browse(self.eye,'file')).grid(row=9,column=0,sticky='ew',pady=(5,0))
        self.gaze_help=ttk.Label(sidebar,text='',style='Muted.TLabel',wraplength=215,justify='left')
        self.gaze_help.grid(row=10,column=0,sticky='w',pady=(8,0))

        work=ttk.Frame(self.experiment_panels)
        self.experiment_panels.add(work,minsize=650,stretch='always')
        work.rowconfigure(2,weight=1)
        work.columnconfigure(0,weight=1)
        heading=ttk.Frame(work)
        heading.grid(row=0,column=0,sticky='ew',pady=(0,6))
        heading.columnconfigure(0,weight=1)
        self.demo_label=ttk.Label(heading,text='Konfiguracja eksperymentu' if self.language_code == 'pl' else 'Experiment setup',style='Heading.TLabel')
        self.demo_label.grid(row=0,column=0,sticky='w')
        self._info_label(heading,'Blok:','gui.block').grid(row=0,column=1,padx=(10,3))
        self.block_combo=ttk.Combobox(heading,textvariable=self.block_name,state='readonly',width=24)
        self.block_combo.grid(row=0,column=2,sticky='e')
        self.block_combo.bind('<<ComboboxSelected>>',self._change_block)
        ttk.Label(heading,text='Projekt:').grid(row=1,column=0,sticky='e',pady=(5,0))
        project_controls=ttk.Frame(heading)
        project_controls.grid(row=1,column=1,columnspan=2,sticky='e',pady=(5,0))
        self.project_combo=ttk.Combobox(project_controls,textvariable=self.project_name,
                                        state='readonly',width=27)
        self.project_combo.pack(side='left')
        self.project_combo.bind('<<ComboboxSelected>>',self._project_changed)
        ttk.Button(project_controls,text='Nowy projekt…',command=self._new_project).pack(side='left',padx=(6,0))
        self.desc_label=ttk.Label(work,text='',style='Muted.TLabel',wraplength=790)
        self.desc_label.grid(row=1,column=0,sticky='w',pady=(0,8))
        self.tabs=ttk.Notebook(work)
        self.tabs.grid(row=2,column=0,sticky='nsew')
        self.pages={}
        for tab in TABS:
            page=ttk.Frame(self.tabs,padding=12)
            self.pages[tab]=page
            self.tabs.add(page,text=tab)
        self.tabs.bind('<<NotebookTabChanged>>',self._on_tab_changed)
        self.tabs.bind('<<NotebookTabChanged>>',self._update_tab_icons, add='+')
        self._update_tab_icons()
        footer=ttk.Frame(work)
        footer.grid(row=3,column=0,sticky='ew',pady=(10,0))
        reset_button=ttk.Button(footer,text='Przywróć oryginał',command=self._reset)
        reset_button.pack(side='left',padx=(0,6))
        self._set_experiment_icon(reset_button, 'reset')
        export_button=ttk.Button(footer,text='Eksportuj YAML…',command=self._export)
        export_button.pack(side='left',padx=(0,6))
        self._set_experiment_icon(export_button, 'export')
        validate_button=ttk.Button(footer,text='Sprawdź konfigurację',command=self._validate)
        validate_button.pack(side='right',padx=(6,0))
        self._set_experiment_icon(validate_button, 'check')
        self._info_icon(footer,'gui.profile').pack(side='right',padx=(3,0))
        save_profile_button=ttk.Button(footer,text='Zapisz profil',style='Accent.TButton',command=self._save)
        save_profile_button.pack(side='right',padx=(6,0))
        self._set_experiment_icon(save_profile_button, 'save', active='ink')
        apply_button=ttk.Button(footer,text='Zastosuj edycję',command=self._apply_button)
        apply_button.pack(side='right',padx=(6,0))
        self._set_compact_icon(apply_button, 'check')
        statusrow=ttk.Frame(self)
        statusrow.grid(row=3,column=0,columnspan=2,sticky='ew',pady=(8,0))
        ttk.Separator(statusrow).pack(fill='x',pady=(0,5))
        ttk.Label(statusrow,textvariable=self.status,style='Muted.TLabel').pack(side='left')
        ttk.Label(statusrow,text='Backend: native Python subprocess · logi w osobnym oknie',style='Muted.TLabel').pack(side='right')

    def _set_compact_icon(self, button, name):
        """Three opt-in 20px icons; leave all other v0.2.14 button sizes alone."""
        cache = getattr(self.root, '_pytracker_compact_icons', None)
        if cache is None:
            cache = {}
            self.root._pytracker_compact_icons = cache
        if name not in cache:
            cache[name] = self._experiment_icon(name).subsample(2, 2)
        button.configure(image=cache[name], compound='left')

    def _update_tab_icons(self, _event=None):
        """Change only the tiny icon on selection; no editor or experiment work."""
        names = {'Dane': 'data', 'Monitor': 'monitor', 'Wygląd': 'appearance',
                 'Instrukcje': 'instructions', 'YAML': 'yaml', 'Uruchomienie': 'launch'}
        try:
            selected = self.tabs.select()
            for name, widget in self.pages.items():
                self.tabs.tab(widget, image=self._experiment_icon(names[name],
                              active=(str(widget) == selected)), compound='left')
        except tk.TclError:
            pass

    def _about(self):
        messagebox.showinfo(self._t('O pytracker-gui'),
            'pytracker-gui v'+__version__ + self._t('\n\nEdytor konfiguracji i launcher 7 projektów startowych.\n'
            'PsychoPy działa w osobnym procesie Python 3.10.\n'
            'Ustawienia są zapisywane w osobnym katalogu profili.'), parent=self.root)

    def _browse(self,var,kind):
        value=filedialog.askdirectory(parent=self.root) if kind=='dir' else filedialog.askopenfilename(parent=self.root)
        if value:var.set(value)

    def _autodetect(self):
        if self.runner.running:return
        if self.demo and not self._maybe_leave():return
        upstream, demo = canonical_roots()
        self.upstream.set(str(upstream)); self.demo_root.set(str(demo))
        self._select_default_eye(force=True)
        self.status.set(self._t('Wykryto ścieżki na podstawie położenia folderu pytracker-gui; sprawdź układ i zapisz.'))
        self._save_paths()
        self._reload()

    def _save_paths(self):
        if self.runner.running:return
        issues = validate_layout(self.upstream.get(), self.demo_root.get())
        if issues:
            messagebox.showwarning(self._t('Niekompletny układ repozytoriów'),
                '\n'.join(self._t(x) for x in issues[:8]) + self._t('\n\nRepozytoria trzeba sklonować we wskazanej strukturze.'), parent=self.root)
            self.status.set(self._t('Repozytoria: niekompletny układ. Ścieżek nie zapisano.'))
            return
        self.settings.update({'demo_root':self.demo_root.get().strip(),
                              'upstream_root':self.upstream.get().strip(),
                              'python':self.python.get().strip(),
                              'language':self.language_code,
                              'help_language':self.help_language_code,
                              'help_language_explicit':self.help_language_explicit})
        try:save_settings(self.home,self.settings)
        except OSError as e: messagebox.showerror(self._t('Błąd zapisu'),str(e),parent=self.root);return
        self.status.set(self._t('Zapisano ścieżki aplikacji (bez modyfikacji repozytoriów).'))

    def _probe(self):
        self.status.set(self._t('Sprawdzanie interpretera…'))
        self.root.update_idletasks()
        info=probe_interpreter(self.python.get())
        if info.get('error'):
            info['error'] = self._t(info['error'])
        details=json.dumps(info,ensure_ascii=False,indent=2)
        messagebox.showinfo(self._t('Diagnostyka środowiska (bez eksperymentu)'),details,parent=self.root)
        if info.get('error'):self.status.set(self._t('Python: błąd diagnostyki'))
        elif info.get('version',[])[:2]!=[3,10]:self.status.set(self._t('Python: wykryta wersja inna niż 3.10'))
        else:self.status.set(self._t('Python 3.10: wykryty. Test runtime wymaga środowiska badawczego.'))

    def _list_select(self,_event=None):
        if self._block_update:return
        indices=self.listbox.curselection()
        if not indices:return
        index=indices[0]
        if self.demo and self.demo.key==CATALOG[index].key:return
        self._select_demo(index)

    def _activate_project(self, demo_key, wanted=None):
        available = self.projects.projects_for(demo_key)
        selected = wanted if wanted in available else (demo_key if demo_key in available else
                    (available[0] if available else demo_key))
        directory = self.projects.ensure(selected, demo_key)
        # One-time import of pre-project profiles; never delete their originals.
        legacy = self.home / 'profiles' / demo_key
        imported = directory / 'profiles' / demo_key
        if selected == demo_key and legacy.is_dir() and not imported.exists():
            import shutil
            shutil.copytree(legacy, imported)
        self._active_project = selected
        self._active_project_demo = demo_key
        self.store = ProfileStore(directory, upstream=self.upstream.get())
        self.project_name.set(selected)
        if hasattr(self, 'project_combo'):
            self.project_combo['values'] = self.projects.projects_for(demo_key)

    def _remember_project(self, demo_key, name):
        # Selection preference is lightweight UI metadata, never experiment I/O.
        self.settings.setdefault('last_projects', {})[demo_key] = name
        try:
            save_settings(self.home, self.settings)
        except OSError:
            pass  # The project itself remains self-contained and selectable.

    def _project_changed(self, _event=None):
        selected = self.project_name.get()
        if self.runner.running:
            self.project_name.set(self._active_project or '')
            return
        if selected == self._active_project or not self.demo:
            return
        if not self._maybe_leave():
            self.project_name.set(self._active_project or '')
            return
        index = CATALOG.index(self.demo)
        try:
            self._activate_project(self.demo.key, selected)
            self._remember_project(self.demo.key, selected)
        except (OSError, ValueError) as exc:
            self.project_name.set(self._active_project or '')
            messagebox.showerror(self._t('Błąd'), str(exc), parent=self.root)
            return
        self.demo = None
        self._select_demo(index, ask=False)

    def _new_project(self):
        if self.runner.running or not self.demo:
            return
        name = simpledialog.askstring(self._t('Nowy projekt'),
                                      self._t('Nazwa projektu (litery, cyfry, _ lub -):'),
                                      parent=self.root)
        if name is None:
            return
        name = name.strip()
        if not self._maybe_leave():
            return
        try:
            self.projects.ensure(name, self.demo.key)
            previous = self._active_project
            self._activate_project(self.demo.key, name)
            self._remember_project(self.demo.key, name)
        except (OSError, ValueError) as exc:
            messagebox.showerror(self._t('Błąd'),str(exc),parent=self.root)
            return
        if previous != name:
            index = CATALOG.index(self.demo)
            self.demo = None
            self._select_demo(index, ask=False)

    def _select_demo(self,index,ask=True):
        if self.runner.running:
            if self.demo is not None:
                self._block_update=True
                self.listbox.selection_clear(0,'end')
                self.listbox.selection_set(CATALOG.index(self.demo))
                self._block_update=False
            return
        old = self.demo
        if ask and old and not self._maybe_leave():
            self._block_update=True
            self.listbox.selection_clear(0,'end')
            self.listbox.selection_set(CATALOG.index(old))
            self._block_update=False
            return
        self.demo=CATALOG[index]
        try:
            requested = (self._active_project if self._active_project_demo == self.demo.key else
                         (self.settings.get('last_projects') or {}).get(self.demo.key))
            self._activate_project(self.demo.key, requested)
        except (OSError, ValueError) as exc:
            self.status.set(str(exc))
            self.loaded=False
            return
        self._block_update=True
        self.listbox.selection_clear(0,'end');self.listbox.selection_set(index)
        self._block_update=False
        self.desc_label.configure(text=f'{self._t(self.demo.description)}  |  '
            f'{self._t("modalność: ")}{self.demo.modality}  |  '
            f'{self._t("backend: ")}{self.demo.engine}')
        self.block_combo['values']=[b.name for b in self.demo.blocks]
        self.block_combo.current(0)
        self.block_name.set(self.demo.blocks[0].name)
        self.active_block_key = self.demo.blocks[0].key
        self.loop_by_block = {b.key:str(b.trials) for b in self.demo.blocks}
        self.loop.set(str(self.demo.blocks[0].trials))
        self.gaze.set('mouse');self.eye.set('');self.voice.set(False);self.raw_data.set(False);self.log_level.set('info')
        self._gaze_changed()
        self.docs={};self.hashes={};self.loaded=False;self.dirty=False
        root=Path(self.demo_root.get()).expanduser()
        try:
            for block in self.demo.blocks:
                doc,h=read_source(root / block.config_relpath)
                self.docs[block.key]=doc;self.hashes[block.key]=h
            result=self.store.load(self.demo.key,self.hashes)
            if result:
                profile, meta, stale=result
                self.docs={k:load_text(txt) for k,txt in profile.items()}
                self.gaze.set(meta.get('gaze','mouse'))
                self.eye.set(meta.get('eye_config',''))
                opts=meta.get('runtime') or {}
                self.voice.set(bool(opts.get('voice',False)))
                self.raw_data.set(bool(opts.get('raw_data',False)))
                if isinstance(opts.get('loops'),dict):
                    self.loop_by_block.update({k:str(v) for k,v in opts['loops'].items() if k in self.loop_by_block})
                elif opts.get('loop') is not None:
                    self.loop_by_block[self.demo.blocks[0].key]=str(opts['loop'])
                self.loop.set(self.loop_by_block[self.demo.blocks[0].key])
                self.log_level.set(opts.get('log_level','info'))
                self._gaze_changed()
                self.status.set(self._t('Załadowano profil')+(self._t(' — ŹRÓDŁO ZMIENIONE: sprawdź ustawienia!') if stale else ''))
            else:self.status.set(self._t('Wczytano konfigurację źródłową; modyfikacje zapisuj wyłącznie w profilu.'))
            self.loaded=True
        except Exception as e:
            self.status.set(self._t('Brak źródła YAML — wskaż katalog projektów startowych i kliknij Wczytaj repo'))
            self.docs={};self.hashes={}
        self.dirty=False
        self.persisted_prefs = (self.gaze.get(), self.eye.get(), self._runtime_opts())
        self._refresh_all()

    def _reload(self):
        if self.runner.running:return
        idx=CATALOG.index(self.demo) if self.demo else 0
        if self.demo and not self._maybe_leave():return
        self.dirty=False
        self.demo=None
        self._select_demo(idx,ask=False)

    def _maybe_leave(self):
        if not self.loaded:return True
        if not self._commit_tab():return False
        preferences=(self.gaze.get(), self.eye.get(), self._runtime_opts())
        if not self.dirty and preferences==self.persisted_prefs:return True
        resp=messagebox.askyesnocancel(self._t('Niezapisane zmiany'),
                  self._t('Zapisano zmiany wyłącznie w pamięci. Zapisać profil przed zmianą projektu startowego?'),parent=self.root)
        if resp is None:return False
        if resp and not self._save():return False
        return True

    def _block(self):
        return self.demo.blocks[self.block_combo.current() if self.block_combo.current()>=0 else 0]

    def _change_block(self,event=None):
        if not self.loaded:return
        if self.runner.running:
            prior=next((b for b in self.demo.blocks if b.key==self.active_block_key),None)
            if prior:self.block_name.set(prior.name)
            return
        if not self._commit_tab():
            prior = next((b for b in self.demo.blocks if b.key == self.active_block_key), None)
            if prior:self.block_name.set(prior.name)
            return
        self.active_block_key = self._block().key
        self.loop.set(self.loop_by_block[self.active_block_key])
        self._refresh_all()

    def _on_tab_changed(self,event=None):
        if self._tab_update or not self.loaded:return
        next_tab=TABS[self.tabs.index(self.tabs.select())]
        if next_tab==self.active_tab:return
        if not self._commit_tab():
            self._tab_update=True
            self.tabs.select(self.pages[self.active_tab]);self._tab_update=False
            return
        self.active_tab=next_tab
        self._render(next_tab)

    def _refresh_all(self):
        self._tab_update=True
        self.active_tab=TABS[self.tabs.index(self.tabs.select())]
        for tab in TABS:self._render(tab)
        self._tab_update=False

    def _render(self,tab):
        self.info_popover.dismiss()
        page=self.pages[tab]
        for child in page.winfo_children():child.destroy()
        if not self.loaded:
            ttk.Label(page,text='Wybierz prawidłowy katalog repozytorium projektów startowych i kliknij „Wczytaj repo”.',
                      wraplength=600).pack(anchor='w',pady=22)
            self._translate_widgets(page)
            return
        doc=self.docs[self._block().key]
        if tab in GROUPS:
            wrap=ttk.Frame(page)
            wrap.pack(fill='both',expand=True)
            wrap.columnconfigure(1,weight=1)
            ttk.Label(wrap,text='Edycja pól istniejącego YAML · zastosuj zmiany przed zapisem',style='Muted.TLabel').grid(row=0,column=0,columnspan=3,sticky='w',pady=(0,12))
            entries={}
            for i,field in enumerate(active_fields(doc,GROUPS[tab]),start=1):
                self._info_label(wrap,field.title,field.path,width=27).grid(row=i,column=0,sticky='w',pady=5)
                v=tk.StringVar(value=to_text(get_value(doc,field.path)))
                if field.kind=='choice':
                    inp=ttk.Combobox(wrap,textvariable=v,values=field.options,state='readonly')
                else:
                    inp=ttk.Entry(wrap,textvariable=v)
                inp.grid(row=i,column=1,sticky='ew',padx=6,pady=5)
                if field.kind=='path':
                    ttk.Button(wrap,text='…',width=3,command=lambda var=v:self._browse_path_field(var)).grid(row=i,column=2,padx=(4,0))
                entries[field.path]=(field,v)
            self.field_vars[tab]=entries
        elif tab=='Instrukcje':
            ttk.Label(page,text='Instrukcje są listami tekstów: każda linia to osobny element YAML.',style='Muted.TLabel').pack(anchor='w',pady=(0,8))
            for key in ('intro','outro'):
                self._info_label(page,f'Instrukcje {key.upper()}','instructions.'+key,style='Heading.TLabel').pack(anchor='w',pady=(4,2))
                text=ScrolledText(page,wrap='word',height=7 if key=='intro' else 4,undo=True)
                style_text(text)
                text.pack(fill='both',expand=True,pady=(0,7))
                text.insert('1.0','\n'.join(get_value(doc,'instructions.'+key) or []))
                if key=='intro':self.intro_editor=text
                else:self.outro_editor=text
        elif tab=='YAML':
            self._info_label(page,'Zaawansowany edytor kopii YAML (z zachowaniem komentarzy i obcych kluczy)','gui.yaml_editor',
                             style='Muted.TLabel').pack(anchor='w',pady=(0,8))
            self.yaml_editor=ScrolledText(page,wrap='none',undo=True,font=('TkFixedFont',10))
            style_text(self.yaml_editor)
            self.yaml_editor.pack(fill='both',expand=True)
            self.yaml_editor.insert('1.0',dump_doc(doc))
            self.raw_dirty=False
            self.yaml_editor.bind('<<Modified>>',self._yaml_modified)
            self.yaml_editor.edit_modified(False)
        elif tab=='Uruchomienie':
            ttk.Label(page,text='Uruchomienie w osobnym procesie Python 3.10',
                      style='Heading.TLabel').pack(anchor='w',pady=(0,12))
            controls=ttk.Frame(page)
            controls.pack(fill='x')
            self._info_label(controls,'Liczba prób','runtime.loop_count',width=21).grid(row=0,column=0,sticky='w',pady=5)
            ttk.Entry(controls,textvariable=self.loop,width=10).grid(row=0,column=1,sticky='w')
            self._info_label(controls,'Log level','runtime.log_level',width=21).grid(row=1,column=0,sticky='w',pady=5)
            ttk.Combobox(controls,textvariable=self.log_level,values=['debug','info','warning','error','critical'],state='readonly',width=16).grid(row=1,column=1,sticky='w')
            ttk.Checkbutton(controls,text='Voice (mikrofon wymagany)',variable=self.voice).grid(row=2,column=0,columnspan=2,sticky='w',pady=5)
            self._info_icon(controls,'runtime.enable_voice').grid(row=2,column=2,sticky='w',padx=7)
            ttk.Checkbutton(controls,text='Raw data (wymaga gaze)',variable=self.raw_data).grid(row=3,column=0,columnspan=2,sticky='w',padx=0,pady=5)
            self._info_icon(controls,'runtime.raw_data').grid(row=3,column=2,sticky='w',padx=7)
            actions=ttk.Frame(page)
            actions.pack(anchor='w',pady=(14,0))
            first_row=ttk.Frame(actions)
            first_row.pack(anchor='w')
            self.start_button=ttk.Button(first_row,text='Uruchom projekt',style='Accent.TButton',command=self._start_run)
            self._set_experiment_icon(self.start_button, 'launch', active='ink')
            self.start_button.pack(side='left',padx=(0,8))
            self.stop_button=ttk.Button(first_row,text='Zatrzymaj projekt',command=self._stop_run)
            self._set_experiment_icon(self.stop_button, 'stop')
            self.stop_button.pack(side='left')
            log_controls=ttk.Frame(actions)
            log_controls.pack(anchor='w',pady=(6,0))
            ttk.Button(log_controls,text='Pokaż logi',command=self._show_run_console).pack(side='left',padx=(0,8))
            self.auto_show_toggle=ttk.Checkbutton(
                log_controls, text='Automatycznie pokazuj logi', variable=self.auto_show_logs,
                command=self._auto_show_logs_changed)
            self.auto_show_toggle.pack(side='left',padx=(0,8))
            ttk.Button(log_controls,text='Podgląd kontraktu uruchomienia',command=self._preview).pack(side='left')
            self._run_state(self.runner.running)
            ttk.Label(page,text='Uruchom projekt: zapisuje kopię bieżącego YAML poza repozytoriami i uruchamia proces.\n'
                      'Wynik procesu i walidacja zebranych danych są raportowane osobno.',
                      wraplength=630,style='Muted.TLabel').pack(anchor='w',pady=(14,0))
        self._translate_widgets(page)

    def _browse_path_field(self,var):
        initial=var.get().strip()
        root=Path(self.demo_root.get()).expanduser()
        from .validation import resolve_path
        resolved=resolve_path(root,initial) if initial else root
        if resolved.is_dir() or 'folder' in str(initial).lower() or not resolved.suffix:
            chosen=filedialog.askdirectory(parent=self.root,initialdir=str(resolved if resolved.is_dir() else root))
        else:
            chosen=filedialog.askopenfilename(parent=self.root,initialdir=str(resolved.parent))
        if chosen:var.set(chosen)

    def _yaml_modified(self,event=None):
        if self.yaml_editor.edit_modified():
            self.raw_dirty=True
            self.yaml_editor.edit_modified(False)

    def _commit_tab(self):
        if not self.loaded:return True
        doc=self.docs[self.active_block_key]
        tab=self.active_tab
        try:
            if tab in GROUPS:
                parsed={path:parse_field(field,var.get()) for path,(field,var) in self.field_vars.get(tab,{}).items()}
                changed=False
                for path,value in parsed.items():
                    if get_value(doc,path)!=value:
                        update_value(doc,path,value);changed=True
                self.dirty |= changed
            elif tab=='Instrukcje' and hasattr(self,'intro_editor') and self.intro_editor.winfo_exists():
                for key,widget in (('intro',self.intro_editor),('outro',self.outro_editor)):
                    val=widget.get('1.0','end-1c').split('\n')
                    old=get_value(doc,'instructions.'+key)
                    if val!=list(old):update_value(doc,'instructions.'+key,val);self.dirty=True
            elif tab=='Uruchomienie':
                old=self.loop_by_block.get(self.active_block_key)
                self.loop_by_block[self.active_block_key]=self.loop.get()
                self.dirty |= (old != self.loop.get())
            elif tab=='YAML' and hasattr(self,'yaml_editor') and self.yaml_editor.winfo_exists() and self.raw_dirty:
                text=self.yaml_editor.get('1.0','end-1c')
                replacement=load_text(text)
                self.dirty |= (dump_doc(replacement)!=dump_doc(doc))
                self.docs[self.active_block_key]=replacement
                self.raw_dirty=False
        except Exception as e:
            messagebox.showerror(self._t('Niepoprawne dane'),self._t(str(e)),parent=self.root)
            return False
        return True

    def _apply_button(self):
        if not self.loaded:return
        if self._commit_tab():
            self.status.set(self._t('Zastosowano zmiany w pamięci. Użyj „Zapisz profil”, aby utrwalić je na dysku.'))
            self._render(self.active_tab)

    def _runtime_opts(self):
        return {'voice':bool(self.voice.get()),'raw_data':bool(self.raw_data.get()),
                'loops':self.loop_by_block.copy(),'log_level':self.log_level.get()}

    def _save(self):
        if not self.loaded:return False
        if not self._commit_tab():return False
        for block in self.demo.blocks:
            try:
                val=int(self.loop_by_block[block.key])
                if val<1 or val>block.trials:raise ValueError()
            except (ValueError,KeyError):
                messagebox.showerror(self._t('Niepoprawna liczba prób'),
                   (f'Block {block.name}: enter a number from 1 to {block.trials}.' if self.language_code == 'en'
                   else f'Blok {block.name}: wpisz liczbę od 1 do {block.trials}.'),parent=self.root)
                return False
        try:
            docs={k:dump_doc(v) for k,v in self.docs.items()}
            location=self.store.save(self.demo.key,docs,self.hashes,self.gaze.get(),self.eye.get(),self._runtime_opts())
        except (OSError,ValueError) as e:
            messagebox.showerror(self._t('Błąd zapisu'),str(e),parent=self.root);return False
        self.dirty=False
        self.persisted_prefs=(self.gaze.get(), self.eye.get(), self._runtime_opts())
        self.status.set(self._t('Zapisano profil: ')+str(location))
        return True

    def _reset(self):
        if not self.loaded:return
        if not messagebox.askyesno(self._t('Przywróć'),
                   self._t('Przywrócić oba bloki (lub pojedynczy YAML) do konfiguracji źródłowej w pamięci?\n'
                   'Zapisany profil na dysku pozostanie do ponownego zapisu.'),parent=self.root):return
        root=Path(self.demo_root.get()).expanduser()
        try:
            self.docs={b.key:read_source(root/b.config_relpath)[0] for b in self.demo.blocks}
        except (OSError,ValueError) as e:messagebox.showerror(self._t('Błąd'),str(e),parent=self.root);return
        self.dirty=True;self._refresh_all()
        self.status.set(self._t('Przywrócono ustawienia źródłowe W PAMIĘCI. Zapisz profil, aby je utrwalić.'))

    def _export(self):
        if not self.loaded or not self._commit_tab():return
        filename=f'{self.demo.key}-{self._block().key}.yaml'
        path=filedialog.asksaveasfilename(title=self._t('Eksport kopii YAML'),initialfile=filename,defaultextension='.yaml',
                                         filetypes=[('YAML','*.yaml'),(self._t('Wszystkie'),'*.*')],parent=self.root)
        if not path:return
        target=Path(path).expanduser().resolve()
        protected={(Path(self.demo_root.get()).expanduser()/b.config_relpath).resolve() for d in CATALOG for b in d.blocks}
        if target in protected:
            messagebox.showerror(self._t('Ochrona źródła'),self._t('Nie można nadpisać oryginalnej konfiguracji projektu startowego.'),parent=self.root);return
        try:
            from .storage import atomic_write
            atomic_write(target,dump_doc(self.docs[self._block().key]).encode('utf-8'))
        except OSError as e:messagebox.showerror(self._t('Błąd eksportu'),str(e),parent=self.root);return
        self.status.set(self._t('Wyeksportowano kopię: ')+str(target))

    def _validate(self):
        if not self.loaded:
            messagebox.showwarning(self._t('Brak danych'),self._t('Wskaż katalog repozytorium projektów startowych, potem kliknij Wczytaj repo.'),parent=self.root);return
        if not self._commit_tab():return
        issues=[Finding('BLOCK',x) for x in validate_layout(self.upstream.get(),self.demo_root.get())]
        issues += check_demo_root(Path(self.demo_root.get()).expanduser(),self.demo)
        for block in self.demo.blocks:
            issues += [Finding(x.level,f'{block.name}: {x.detail}') for x in
                       validate_config(self.docs[block.key],Path(self.demo_root.get()).expanduser(),self.demo.modality)]
        if self.gaze.get()=='tobii' and (not self.eye.get() or not Path(self.eye.get()).is_file()):
            issues.append(Finding('BLOCK','Tobii: brak wskazanego pliku ioHub YAML'))
        if self.gaze.get()=='mouse' and (not self.eye.get() or not Path(self.eye.get()).is_file()):
            issues.append(Finding('WARN','MouseGaze: plik ioHub YAML nie został wskazany/nie istnieje (wymagany do startu)'))
        if self.gaze.get()=='none':
            issues.append(Finding('WARN','NO_GAZE: upstream nadal odczytuje plik ioHub YAML; należy wskazać istniejący przed startem'))
        if self.voice.get():issues.append(Finding('WARN','Voice: obsługa tego trybu w adapterach nie została zweryfikowana'))
        if self.raw_data.get():issues.append(Finding('WARN','Raw data: obsługa trybu w adapterach nie została zweryfikowana'))
        blocked=sum(x.level=='BLOCK' for x in issues)
        warn=sum(x.level=='WARN' for x in issues)
        lines=[f'{self._t("PRE-FLIGHT STATYCZNY · ")}{self.demo.label} [{self.demo.variant}]',
               f'BLOCK={blocked}  WARN={warn}  |  {self._t("brak testów runtime/hardware")}','']
        lines += [f'[{x.level}] {self._t(x.detail)}' for x in issues]
        self._show_report(self._t('Kontrola konfiguracji'), '\n'.join(lines))
        self.status.set(f'{self._t("Walidacja statyczna: ")}{blocked} BLOCK / {warn} WARN{self._t(". Runtime: NOT RUN.")}')

    def _preview(self):
        if not self.loaded or not self._commit_tab():return
        demo=self.demo
        entries=[]
        for block in demo.blocks:
            entries.append({'block':block.name,'source_config':block.config_relpath,
                            'profile_config':str(self.store.profile_dir(demo.key)/(block.key+'.yaml')),
                            'default_trials':block.trials})
        variant_ids={'test_en':'test_demo','ux_en':'ux_ab_demo','ux_pl':'ux_ab_demo',
                     'ts_machine_pv':'timeseries_noise_demo','search_en':'text_search_demo',
                     'search_pl':'text_search_demo','image_en':'image_semantic_demo'}
        bash_command='bash tobii-pytracker-demo/tools/run-demo.sh '+variant_ids[demo.key]
        if demo.key in ('ux_pl','search_pl'):bash_command+=' pl'
        info={'DEMO':demo.label,'VARIANT':demo.variant,'BACKEND_PLAN':demo.engine,
              'cwd':self.demo_root.get(),'interpreter':self.python.get(),'upstream':self.upstream.get(),
              'repository_parent':self.upstream.get(),
              'original_demo_command_from_upstream_root':bash_command,
              'original_command_ignores_gui_profile_and_selected_gaze_flags':True,
              'gui_launch_uses_current_yaml_snapshot_and_selected_runtime_flags':True,
              'gaze':self.gaze.get(),'iohub_yaml':self.eye.get(),'settings':self._runtime_opts(),
              'blocks_order':entries,'ready_to_execute':self.loaded}
        self._show_report(self._t('Plan uruchomienia (nie wykonuje)'), json.dumps(info,indent=2,ensure_ascii=False))

    def _select_default_eye(self, force=False):
        selected=self.eye.get().strip()
        up=Path(self.upstream.get()).expanduser()
        default=default_eye_config(up,self.gaze.get())
        known={str(default_eye_config(up,mode)) for mode in ('none','mouse','tobii')}
        if force or not selected or selected in known:
            self.eye.set(str(default))

    def _gaze_changed(self):
        self._select_default_eye()
        mode=self.gaze.get()
        message={'none':'Bez gaze: odpowiedzi myszą pozostają dostępne. ioHub YAML nadal będzie wymagany przez upstream.',
                 'mouse':'MouseGaze: trzymaj PRAWY przycisk, aby symulować gaze; puść przed LEWYM kliknięciem odpowiedzi.',
                 'tobii':'Tobii: wymagane urządzenie i jego własny plik ioHub. Połączenie nie jest jeszcze testowane.'}
        if hasattr(self,'gaze_help'):self.gaze_help.configure(text=self._t(message.get(mode,'')))

    def _show_report(self,title,text):
        popup=tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry('830x530')
        popup.transient(self.root)
        popup.configure(background=COLORS['window'])
        out=ScrolledText(popup,wrap='word',font=('TkFixedFont',10))
        style_text(out)
        out.pack(fill='both',expand=True,padx=12,pady=12)
        out.insert('1.0',text)
        out.configure(state='disabled')
        ttk.Button(popup,text=self._t('Zamknij'),command=popup.destroy).pack(pady=(0,12))

    def _auto_show_logs_changed(self):
        """Store only the local display preference; never alter experiment settings."""
        choice = self.auto_show_logs.get()
        new_settings = dict(self.settings)
        new_settings['auto_show_logs'] = choice
        try:
            save_settings(self.home, new_settings)
        except OSError as exc:
            self.auto_show_logs.set(not choice)
            messagebox.showerror(self._t('Błąd zapisu'), str(exc), parent=self.root)
            return
        self.settings = new_settings
        if not choice and self.run_console is not None and self.run_console.winfo_exists():
            # Disabling auto-display also stops Tk text rendering immediately.
            self.run_console.destroy()
            self.run_log = None

    def _log_view_destroyed(self, event):
        # Tk may destroy the editor directly in a test or host; release OS temp.
        if event.widget is self and self._run_spool is not None:
            self._run_spool.close()
            self._run_spool = None

    def _reset_run_log_capture(self):
        self._last_experiment_log = None
        if self._run_spool is not None:
            self._run_spool.close()
        self._run_spool = None
        self._run_spool_failed = False
        self._run_display_lines = []
        self._run_preview_chars = 0
        self._run_preview_lines = 0
        if self.run_log is not None and self.run_log.winfo_exists():
            self.run_log.delete('1.0', 'end')

    def _run_state(self, running):
        if hasattr(self,'start_button') and self.start_button.winfo_exists():
            self.start_button.configure(state=('disabled' if running else 'normal'))
        if hasattr(self,'stop_button') and self.stop_button.winfo_exists():
            self.stop_button.configure(state=('normal' if running else 'disabled'))

    def _start_run(self):
        if self.runner.running:
            return
        if not self.loaded or not self._commit_tab():
            return
        # No duplicate validation logic: the run manifest is only published if
        # all eight-path/layout, YAML, gaze, and trial-count gates pass.
        info=probe_interpreter(self.python.get().strip())
        if info.get('error') or info.get('version', [])[:2] != [3,10] or not info.get('modules', {}).get('tobii_pytracker') or not info.get('modules', {}).get('psychopy'):
            messagebox.showerror(self._t('Nie można uruchomić'),
                                 self._t('Wybierz Python 3.10 z działającymi pakietami tobii_pytracker i psychopy.')+'\n'+json.dumps(info,ensure_ascii=False,indent=2), parent=self.root)
            return
        try:
            manifest=prepare_run(home=self.home, project_dir=self.store.home,
                        gui_settings={'language': self.language_code,
                                      'help_language': self.help_language_code,
                                      'help_language_explicit': self.help_language_explicit},
                        demo_key=self.demo.key,docs=self.docs,
                        loops=self.loop_by_block,demo_root=self.demo_root.get(),
                        upstream=self.upstream.get(),python=self.python.get(),
                        gaze=self.gaze.get(),eye=self.eye.get(),voice=self.voice.get(),
                        raw_data=self.raw_data.get(),log_level=self.log_level.get())
            # Keep the latest reusable profile inside the portable project.
            self.store.save(self.demo.key, {k: dump_doc(v) for k, v in self.docs.items()},
                            self.hashes, self.gaze.get(), self.eye.get(), self._runtime_opts())
            self.runner.start(manifest)
            self.dirty=False
            self.persisted_prefs=(self.gaze.get(), self.eye.get(), self._runtime_opts())
        except (OSError,ValueError,RuntimeError) as exc:
            messagebox.showerror(self._t('Nie można uruchomić'),str(exc),parent=self.root)
            return
        self._active_manifest = manifest
        self._reset_run_log_capture()
        self._run_state(True)
        if self.auto_show_logs.get():
            self._show_run_console()
        elif self.run_console is not None and self.run_console.winfo_exists():
            self.run_console.destroy()
            self.run_log = None
        # [RUN] is emitted by ExperimentRunner into the single journal and GUI queue.
        self.status.set(self._t('Eksperyment uruchomiony; wyniki i logi pozostają w osobnych katalogach.'))
        self._poll_run()

    def _show_run_console(self):
        if self.run_console is not None and self.run_console.winfo_exists():
            self.run_console.lift()
            return
        popup=tk.Toplevel(self.root)
        popup.title('pytracker-gui · '+self._t('Dziennik eksperymentu'))
        popup.geometry('850x490')
        self.run_console=popup
        popup.configure(background=COLORS['window'])
        self.run_log=ScrolledText(popup,wrap='word',font=('TkFixedFont',10))
        style_text(self.run_log)
        self.run_log.pack(fill='both',expand=True,padx=10,pady=10)
        if self._run_display_lines:
            self.run_log.insert('1.0',''.join(self._run_display_lines))
            self.run_log.see('end')
        controls=ttk.Frame(popup)
        controls.pack(fill='x',padx=10,pady=(0,10))
        ttk.Button(controls,text=self._t('Zatrzymaj projekt'),command=self._stop_run).pack(side='left')
        ttk.Button(controls,text=self._t('Kopiuj cały log'),command=self._copy_run_log).pack(side='left',padx=(8,0))
        ttk.Button(controls,text=self._t('Zamknij okno logów'),command=popup.destroy).pack(side='right')

    def _copy_run_log(self):
        """Copy exactly the entire visible experiment log, including GUI status lines."""
        if self.run_log is None or not self.run_log.winfo_exists():
            return
        # Reading the complete text is a user-requested operation only. The
        # 256-KiB live preview limit must not silently truncate Copy entire log.
        try:
            if self._run_spool is not None:
                cursor = self._run_spool.tell()
                try:
                    self._run_spool.seek(0)
                    content = self._run_spool.read()
                finally:
                    self._run_spool.seek(cursor)
            elif self._last_experiment_log is not None and self._last_experiment_log.is_file():
                content = self._last_experiment_log.read_text(encoding='utf-8')
            else:
                content = self.run_log.get('1.0', 'end-1c')
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
        except (OSError, ValueError, tk.TclError) as exc:
            messagebox.showerror(self._t('Błąd kopiowania logu'),str(exc),parent=self.run_console)
            return
        self.status.set(self._t('Skopiowano cały log eksperymentu do schowka.'))

    def _append_run_log(self, line):
        """Capture complete log in a bounded spool; render only a bounded tail."""
        if self._run_spool is None and not self._run_spool_failed:
            try:
                self._run_spool = tempfile.SpooledTemporaryFile(
                    mode='w+t', max_size=262144, encoding='utf-8', newline='')
            except OSError as exc:
                self._run_spool_failed = True
                self.status.set(self._t('Nie udało się zapisać logu projektu: ') + str(exc))
        if self._run_spool is not None and not self._run_spool_failed:
            try:
                self._run_spool.write(line)
            except (OSError, ValueError) as exc:
                self._run_spool_failed = True
                self.status.set(self._t('Nie udało się zapisać logu projektu: ') + str(exc))
        # A single unusually long message must not bypass the preview limit.
        preview = line[-262144:]
        line_count = max(1, preview.count('\n'))
        self._run_display_lines.append(preview)
        self._run_preview_chars += len(preview)
        self._run_preview_lines += line_count
        dropped = 0
        while (self._run_preview_chars > 262144 or self._run_preview_lines > 2000):
            removed = self._run_display_lines[dropped]
            self._run_preview_chars -= len(removed)
            self._run_preview_lines -= max(1, removed.count('\n'))
            dropped += 1
        if dropped:
            del self._run_display_lines[:dropped]
        if self.run_log is not None and self.run_log.winfo_exists():
            if dropped:
                self.run_log.delete('1.0', 'end')
                self.run_log.insert('1.0', ''.join(self._run_display_lines))
            else:
                self.run_log.insert('end', preview)
            self.run_log.see('end')

    def _poll_run(self):
        import queue
        final=None
        try:
            while True:
                kind,value=self.runner.events.get_nowait()
                if kind=='log':self._append_run_log(value)
                elif kind=='state':
                    self.status.set(value)
                elif kind=='done':
                    final=value
        except queue.Empty:
            pass
        if final is not None:
            self._save_finished_experiment_log()
            self.status.set(self._t('Wynik eksperymentu: ')+final)
            self._run_state(False)
        elif self.runner.running or not self.runner.events.empty():
            self._run_poll_id=self.root.after(100,self._poll_run)
        else:
            self._run_state(False)

    def _save_finished_experiment_log(self):
        """No second archive: the runner's background writer owns the single log.

        Keep the existing 256-KiB GUI spool until next run/GUI close, so the
        user-requested Copy entire log still works before async finalization.
        """
        if self._active_manifest is None:
            return
        journal = self.runner._journal
        if journal is not None:
            self._last_experiment_log = journal.complete_path if journal.complete_path.exists() else journal.partial_path
        self._active_manifest = None

    def _stop_run(self):
        if not self.runner.running:return
        if messagebox.askyesno(self._t('Zatrzymać eksperyment?'),
                self._t('Przerwanie sesji może pozostawić niekompletne dane. Zatrzymać proces?'),parent=self.root):
            self.runner.stop()

    def request_close(self):
        if self.runner.running:
            if not messagebox.askyesno(self._t('Zatrzymać eksperyment?'),
                self._t('Zamknięcie GUI przerwie trwającą sesję. Kontynuować?'),parent=self.root):
                return
            self.runner.stop(wait=True)
            # Drain the final statuses and publish the final GUI log before exit.
            if self.runner.running:
                messagebox.showwarning(self._t('Zatrzymać eksperyment?'),
                                       self._t('Proces nadal się zatrzymuje. Poczekaj na zakończenie.'),
                                       parent=self.root)
                return
            self._poll_run()
        if self._maybe_leave():
            self.info_popover.dismiss()
            if self._run_spool is not None:
                self._run_spool.close()
                self._run_spool = None
            self.root.destroy()


def main():
    _enable_hidpi_awareness()
    root=tk.Tk()
    _configure_tk_scaling(root)
    from .shell import AppShell
    AppShell(root)
    root.mainloop()
