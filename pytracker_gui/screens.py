"""Lightweight, independent future module screens.

These frames intentionally perform no filesystem, runtime, or background work.
They are constructed by AppShell only after the user first visits each screen.
"""
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from .theme import icon, COLORS, factory_palette, valid_hex_color
from .parameter_help import get_parameter_help, parameter_catalog
from .i18n import translate
from .layout import canonical_roots
from .upstream_docs import UpstreamRstBrowser
from .demo_docs import DemoProjectDocsBrowser
from .gui_docs import GuiDocumentationBrowser


SCREEN_COPY = {
    'logs': (
        'Logi eksperymentów',
        'Historia logów projektów będzie dostępna w przyszłej wersji.',
        'Obecne okno Experiment log jest nadal dostępne na ekranie Eksperyment.',
    ),
    'statistics': (
        'Statystyki projektu',
        'Statystyki i wykresy zostaną dodane w przyszłej wersji.',
        'Ten ekran nie odczytuje logów, wyników ani danych eksperymentu.',
    ),
}


GUI_SETTINGS_TEXTS = {
    'pl': {
        'subtitle': 'Ustawienia aplikacji i ścieżki używane przez GUI · bez konfiguracji eksperymentu',
        'window': 'Okno i wygląd', 'paths': 'Ścieżki i środowisko', 'preferences': 'Preferencje',
        'window_size': 'Rozmiar przy uruchomieniu', 'save': 'Zapisz rozmiar',
        'window_hint': 'Zmiana obowiązuje od następnego uruchomienia. Na mniejszych ekranach rozmiar jest ograniczany do dostępnego miejsca.',
        'tile_size': 'Kafelki głównego panelu', 'tile_value': '546 × 365 px · stały rozmiar',
        'gui_home': 'Katalog danych GUI', 'projects_root': 'Historia projektów',
        'demo_root': 'Repozytorium dem', 'upstream_root': 'Oryginalne repozytorium',
        'python': 'Interpreter Python',
        'path_hint': 'Ścieżki można zmieniać i zapisywać w sekcji Environment ekranu Experiment.',
        'language': 'Język interfejsu', 'help_language': 'Język podpowiedzi',
        'auto_logs': 'Auto-show Logs', 'journal': 'Dziennik konsoli',
        'journal_value': 'Jeden log narastający · .log / .log.part',
        'saved': 'Rozmiar zapisany. Zostanie użyty przy następnym uruchomieniu.',
        'error': 'Nie udało się zapisać ustawień:',
        'colors': 'Kolory interfejsu',
        'colors_hint': 'Istniejące parametry ICON_COLOR i COLORS. Wprowadź #RRGGBB; zmiany po ponownym uruchomieniu.',
        'save_colors': 'Zapisz kolory', 'reset_colors': 'Przywróć domyślne wartości',
        'colors_saved': 'Kolory zapisane. Uruchom GUI ponownie, aby je zastosować.',
        'colors_error': 'Nieprawidłowa wartość #RRGGBB dla:',
    },
    'en': {
        'subtitle': 'Application settings and GUI paths · separate from experiment configuration',
        'window': 'Window & appearance', 'paths': 'Paths & environment', 'preferences': 'Preferences',
        'window_size': 'Startup window size', 'save': 'Save window size',
        'window_hint': 'Takes effect on the next launch. Smaller screens clamp the window to available space.',
        'tile_size': 'Home dashboard tiles', 'tile_value': '546 × 365 px · fixed size',
        'gui_home': 'GUI data directory', 'projects_root': 'Project history',
        'demo_root': 'Demo repository', 'upstream_root': 'Original upstream repository',
        'python': 'Python interpreter',
        'path_hint': 'Edit and save repository paths in Experiment → Environment.',
        'language': 'Interface language', 'help_language': 'Tooltip language',
        'auto_logs': 'Auto-show Logs', 'journal': 'Console journal',
        'journal_value': 'Single incremental log · .log / .log.part',
        'saved': 'Startup size saved. It will apply on the next launch.',
        'error': 'Could not save settings:',
        'colors': 'Interface colors',
        'colors_hint': 'Existing ICON_COLOR and COLORS parameters. Enter #RRGGBB; applied on next launch.',
        'save_colors': 'Save colors', 'reset_colors': 'Restore defaults',
        'colors_saved': 'Colors saved. Restart GUI to apply them.',
        'colors_error': 'Invalid #RRGGBB value for:',
    },
}



class PlaceholderScreen(ttk.Frame):
    """One inactive module; no polling, callbacks or imported analysis packages."""

    def __init__(self, master, screen_id, language='pl'):
        if screen_id not in SCREEN_COPY:
            raise ValueError('Unknown screen: ' + screen_id)
        super().__init__(master, padding=24)
        self.screen_id = screen_id
        self.title_label = ttk.Label(self, style='Heading.TLabel')
        self.title_label.pack(anchor='w', pady=(0, 14))
        self.message_label = ttk.Label(self, wraplength=730, justify='left')
        self.message_label.pack(anchor='w', pady=(0, 12))
        self.note_label = ttk.Label(self, style='Muted.TLabel', wraplength=730, justify='left')
        self.note_label.pack(anchor='w')
        self.set_language(language)

    def set_language(self, language):
        title, message, note = SCREEN_COPY[self.screen_id]
        self.title_label.configure(text=translate(title, language))
        self.message_label.configure(text=translate(message, language))
        self.note_label.configure(text=translate(note, language))


class DashboardScreen(ttk.Frame):
    """Four image-backed buttons at a fixed pixel size; only created on demand.

    Dashboard PNGs are pre-rendered assets, so resizing the application never
    resamples, regenerates or resizes any tile image. No Pillow at runtime.
    """

    TILES = (
        ('experiment', 'Eksperyment', 'experiment'),
        ('logs', 'Logi', 'logs'),
        ('statistics', 'Statystyki', 'statistics'),
        ('manual', 'Manual', 'manual'),
    )
    TILE_SIZE = (546, 365)

    def __init__(self, master, on_select, language='pl', root=None):
        super().__init__(master, padding=24)
        self.on_select = on_select
        self.title_label = ttk.Label(self, style='DashboardTitle.TLabel')
        self.title_label.pack(anchor='w', pady=(0, 15))
        viewport = ttk.Frame(self)
        self.viewport = viewport
        viewport.pack(fill='both', expand=True)
        # A passive viewport permits access to every fixed tile if the user
        # shrinks the window below the initial 2x2 layout. Scrollbars are only
        # shown on overflow; the board and images are never resized.
        self.canvas = tk.Canvas(viewport, background=COLORS['surface'],
                                borderwidth=0, highlightthickness=0)
        self.hscroll = ttk.Scrollbar(viewport, orient='horizontal', command=self.canvas.xview)
        self.vscroll = ttk.Scrollbar(viewport, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hscroll.set, yscrollcommand=self.vscroll.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        board = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=board, anchor='nw')
        board.bind('<Configure>', self._update_viewport)
        self.canvas.bind('<Configure>', self._update_viewport)
        viewport.bind('<Configure>', self._update_viewport)
        # No grid weights or sticky='nsew': an enlarged window leaves free space,
        # and a smaller window cannot stretch or compress any of the four tiles.
        style = ttk.Style(self)
        style.configure('DashboardImage.TButton', padding=0, borderwidth=0,
                        relief='flat', background=COLORS['surface_alt'])
        # The image is the entire button surface, not an inset of a themed border.
        style.layout('DashboardImage.TButton', [('Button.label', {'sticky': 'nswe'})])
        self.tile_buttons = {}
        self._tile_images = {}
        assets = Path(__file__).with_name('assets')
        master_root = root or self.winfo_toplevel()
        for index, (screen_id, _, _) in enumerate(self.TILES):
            image = tk.PhotoImage(master=master_root, file=str(assets / f'dashboard-{screen_id}.png'))
            if (image.width(), image.height()) != self.TILE_SIZE:
                raise ValueError('Incorrect dashboard tile image size: ' + screen_id)
            self._tile_images[screen_id] = image
            tile = ttk.Button(board, style='DashboardImage.TButton',
                              image=image, compound='none', cursor='hand2',
                              command=lambda key=screen_id: self.on_select(key))
            tile.grid(row=index // 2, column=index % 2, padx=9, pady=9)
            self.tile_buttons[screen_id] = tile
        self.set_language(language)

    def _update_viewport(self, _event=None):
        bbox = self.canvas.bbox('all')
        if not bbox:
            return
        self.canvas.configure(scrollregion=bbox)
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        available_w = self.viewport.winfo_width()
        available_h = self.viewport.winfo_height()
        # Calculate against the *unobstructed* viewport, otherwise a transient
        # scrollbar can keep both scrollbars visible at the initial exact fit.
        overflow_x = width > available_w
        overflow_y = height > available_h - (self.hscroll.winfo_reqheight() if overflow_x else 0)
        overflow_x = width > available_w - (self.vscroll.winfo_reqwidth() if overflow_y else 0)
        overflow_y = height > available_h - (self.hscroll.winfo_reqheight() if overflow_x else 0)
        if overflow_x and not self.hscroll.winfo_manager():
            self.hscroll.pack(side='bottom', fill='x', before=self.canvas)
        elif not overflow_x and self.hscroll.winfo_manager():
            self.hscroll.pack_forget()
        if overflow_y and not self.vscroll.winfo_manager():
            self.vscroll.pack(side='right', fill='y', before=self.canvas)
        elif not overflow_y and self.vscroll.winfo_manager():
            self.vscroll.pack_forget()

    def set_language(self, language):
        self.title_label.configure(text=translate('Wybierz ekran', language))
        # Text remains available in button metadata, including in both locales.
        # The visible captions are part of the four approved English images.
        for screen_id, title, _ in self.TILES:
            self.tile_buttons[screen_id].configure(text=translate(title, language))


class GuiSettingsScreen(ttk.Frame):
    """Lightweight GUI settings view; never edits experiment YAML or repository data."""

    WINDOW_PRESETS = ('940 × 650', '1100 × 800', '1300 × 960', '1429 × 1097', '1600 × 1000')

    def __init__(self, master, settings_provider, save_window_size, language='pl', save_colors=None):
        super().__init__(master, padding=(15, 12))
        self.settings_provider = settings_provider
        self.save_window_size = save_window_size
        self.save_colors = save_colors
        self._color_vars = {}
        self._color_swatches = {}
        self.language = language if language in GUI_SETTINGS_TEXTS else 'pl'
        self.window_size_var = tk.StringVar(self)
        self._path_vars = {}
        self._pref_labels = {}
        self._section_titles = {}
        self._labels = {}
        self._build()
        self.refresh()

    def tr(self, key):
        return GUI_SETTINGS_TEXTS[self.language][key]

    def _build(self):
        # These styles are local to the new page, without modifying global ttk palette.
        style = ttk.Style(self)
        style.configure('GuiSettingsTitle.TLabel', background=COLORS['surface'],
                        foreground=COLORS['text'], font=('TkDefaultFont', 17, 'bold'))
        style.configure('GuiSettingsSubtitle.TLabel', background=COLORS['surface'],
                        foreground=COLORS['muted'], font=('TkDefaultFont', 11))
        self.title = ttk.Label(self, style='GuiSettingsTitle.TLabel', text='GUI Settings')
        self.title.pack(anchor='w')
        self.subtitle = ttk.Label(self, style='GuiSettingsSubtitle.TLabel', text=self.tr('subtitle'))
        self.subtitle.pack(anchor='w', pady=(3, 10))
        ttk.Separator(self).pack(fill='x', pady=(0, 10))
        # One native scroll surface: the new bottom card remains reachable even
        # on smaller displays. No timer, watcher or resize-time image work.
        view = ttk.Frame(self)
        view.pack(fill='both', expand=True)
        self.settings_canvas = tk.Canvas(view, bg=COLORS['surface'], bd=0, highlightthickness=0)
        scroll = ttk.Scrollbar(view, orient='vertical', command=self.settings_canvas.yview)
        self.settings_canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        self.settings_canvas.pack(side='left', fill='both', expand=True)
        self.sections_frame = ttk.Frame(self.settings_canvas)
        self._canvas_window = self.settings_canvas.create_window(
            (0, 0), window=self.sections_frame, anchor='nw')
        self.sections_frame.bind('<Configure>', self._sync_scrollregion)
        self.settings_canvas.bind('<Configure>', self._sync_canvas_width)
        self.window_card = self._card('window')
        control = tk.Frame(self.window_card, bg=COLORS['field'])
        control.pack(fill='x', padx=15, pady=(0, 7))
        self._caption(control, 'window_size').pack(side='left', padx=(0, 15))
        self.preset_combo = ttk.Combobox(control, textvariable=self.window_size_var,
                                          state='readonly', width=17, values=self.WINDOW_PRESETS)
        self.preset_combo.pack(side='left', padx=(0, 12))
        self.save_button = ttk.Button(control, text=self.tr('save'), command=self._save)
        self.save_button.pack(side='left')
        self.status = ttk.Label(self.window_card, text='', style='GuiSettingsSubtitle.TLabel')
        self.status.pack(anchor='w', padx=15, pady=(0, 5))
        self.window_hint = self._hint(self.window_card, 'window_hint')
        self.window_hint.pack(anchor='w', padx=15, pady=(0, 10))
        tiles = tk.Frame(self.window_card, bg=COLORS['field'])
        tiles.pack(fill='x', padx=15, pady=(0, 12))
        self._caption(tiles, 'tile_size').pack(side='left')
        self.tile_value = tk.Label(tiles, text=self.tr('tile_value'), bg=COLORS['field'],
                                   fg=COLORS['text'], font=('Segoe UI', 10))
        self.tile_value.pack(side='left', padx=(20, 0))

        self.paths_card = self._card('paths')
        for key in ('gui_home', 'projects_root', 'demo_root', 'upstream_root', 'python'):
            line = tk.Frame(self.paths_card, bg=COLORS['field'])
            line.pack(fill='x', padx=15, pady=(0, 8))
            self._caption(line, key, width=25).pack(side='left', padx=(0, 14))
            var = tk.StringVar(self)
            entry = ttk.Entry(line, textvariable=var, state='readonly')
            entry.pack(side='left', fill='x', expand=True)
            self._path_vars[key] = var
        self.path_hint = self._hint(self.paths_card, 'path_hint')
        self.path_hint.pack(anchor='w', padx=15, pady=(0, 12))

        self.prefs_card = self._card('preferences')
        for key in ('language', 'help_language', 'auto_logs', 'journal'):
            line = tk.Frame(self.prefs_card, bg=COLORS['field'])
            line.pack(fill='x', padx=15, pady=(0, 9))
            self._caption(line, key, width=25).pack(side='left', padx=(0, 14))
            value = tk.Label(line, text='', bg=COLORS['field'], fg=COLORS['text'],
                             anchor='w', font=('Segoe UI', 10))
            value.pack(side='left')
            self._pref_labels[key] = value

        # Bottom panel edits ONLY already-existing theme.py parameters.
        self.colors_card = self._card('colors')
        self.colors_hint = self._hint(self.colors_card, 'colors_hint')
        self.colors_hint.pack(anchor='w', padx=15, pady=(0, 9))
        editor = tk.Frame(self.colors_card, bg=COLORS['field'])
        editor.pack(fill='x', padx=15)
        keys = ['ICON_COLOR'] + list(COLORS)
        for index, key in enumerate(keys):
            col = index // 8
            row = index % 8
            line = tk.Frame(editor, bg=COLORS['field'])
            line.grid(row=row, column=col, sticky='w', padx=(0, 38), pady=(0, 7))
            tk.Label(line, text=key, width=15, anchor='w', bg=COLORS['field'],
                     fg=COLORS['muted'], font=('TkDefaultFont', 10)).pack(side='left')
            var = tk.StringVar(self)
            entry = ttk.Entry(line, textvariable=var, width=10)
            entry.pack(side='left', padx=(5, 7))
            swatch = tk.Label(line, width=3, bg=COLORS['field'], relief='solid',
                              bd=1, highlightbackground=COLORS['border'])
            swatch.pack(side='left')
            self._color_vars[key] = var
            self._color_swatches[key] = swatch
        actions = ttk.Frame(self.colors_card)
        actions.pack(anchor='w', padx=15, pady=(7, 5))
        self.save_colors_button = ttk.Button(actions, text=self.tr('save_colors'),
                                             command=self._save_colors)
        self.save_colors_button.pack(side='left', padx=(0, 10))
        self.reset_colors_button = ttk.Button(actions, text=self.tr('reset_colors'),
                                              command=self._reset_colors)
        self.reset_colors_button.pack(side='left')
        self.colors_status = ttk.Label(self.colors_card, style='GuiSettingsSubtitle.TLabel')
        self.colors_status.pack(anchor='w', padx=15, pady=(0, 9))

    def _sync_scrollregion(self, _event=None):
        self.settings_canvas.configure(scrollregion=self.settings_canvas.bbox('all'))

    def _sync_canvas_width(self, event):
        self.settings_canvas.itemconfigure(self._canvas_window, width=event.width)

    def _card(self, title_key):
        card = tk.Frame(self.sections_frame, bg=COLORS['field'], highlightthickness=1,
                        highlightbackground=COLORS['border'])
        card.pack(fill='x', pady=(0, 11))
        heading = tk.Label(card, text=self.tr(title_key), bg=COLORS['field'],
                           fg=COLORS['text'], font=('Segoe UI', 12, 'bold'), anchor='w')
        heading.pack(fill='x', padx=15, pady=(12, 12))
        self._section_titles[title_key] = heading
        return card

    def _caption(self, parent, key, **kwargs):
        label = tk.Label(parent, text=self.tr(key), bg=COLORS['field'],
                         fg=COLORS['muted'], font=('Segoe UI', 10, 'bold'), anchor='w', **kwargs)
        self._labels[key] = label
        return label

    def _hint(self, parent, key):
        label = tk.Label(parent, text=self.tr(key), bg=COLORS['field'],
                         fg=COLORS['muted'], font=('Segoe UI', 10), anchor='w', justify='left')
        return label

    def set_language(self, language):
        self.language = language if language in GUI_SETTINGS_TEXTS else 'pl'
        self.subtitle.configure(text=self.tr('subtitle'))
        for key, widget in self._section_titles.items():
            widget.configure(text=self.tr(key))
        for key, widget in self._labels.items():
            widget.configure(text=self.tr(key))
        self.window_hint.configure(text=self.tr('window_hint'))
        self.path_hint.configure(text=self.tr('path_hint'))
        self.tile_value.configure(text=self.tr('tile_value'))
        self.save_button.configure(text=self.tr('save'))
        self.colors_hint.configure(text=self.tr('colors_hint'))
        self.save_colors_button.configure(text=self.tr('save_colors'))
        self.reset_colors_button.configure(text=self.tr('reset_colors'))
        self.refresh()

    def refresh(self):
        settings = self.settings_provider()
        self.window_size_var.set(settings.get('window_size', '1429 × 1097'))
        for key, var in self._path_vars.items():
            var.set(str(settings.get(key, '—')))
        for key, widget in self._pref_labels.items():
            widget.configure(text=(self.tr('journal_value') if key == 'journal'
                                   else str(settings.get(key, '—'))))
        self.status.configure(text='')
        current_palette = factory_palette()
        icon_color = settings.get('ICON_COLOR', current_palette['ICON_COLOR'])
        saved_colors = settings.get('COLORS', {})
        if not isinstance(saved_colors, dict):
            saved_colors = {}
        for key, var in self._color_vars.items():
            candidate = icon_color if key == 'ICON_COLOR' else saved_colors.get(
                key, current_palette['COLORS'][key])
            value = candidate if valid_hex_color(candidate) else (
                current_palette['ICON_COLOR'] if key == 'ICON_COLOR' else current_palette['COLORS'][key])
            var.set(value.upper())
            self._color_swatches[key].configure(bg=value)
        self.colors_status.configure(text='')

    def _reset_colors(self):
        defaults = factory_palette()
        for key, var in self._color_vars.items():
            value = defaults['ICON_COLOR'] if key == 'ICON_COLOR' else defaults['COLORS'][key]
            var.set(value.upper())
            self._color_swatches[key].configure(bg=value)
        self.colors_status.configure(text='')

    def _save_colors(self):
        # Validate the ENTIRE existing palette before performing any disk write.
        values = {key: var.get().strip().upper() for key, var in self._color_vars.items()}
        bad = next((key for key, value in values.items() if not valid_hex_color(value)), None)
        if bad:
            self.colors_status.configure(text=self.tr('colors_error') + ' ' + bad)
            return
        if self.save_colors is None:
            return
        try:
            self.save_colors(values['ICON_COLOR'], {key: values[key] for key in COLORS})
        except (OSError, ValueError) as exc:
            self.colors_status.configure(text=self.tr('error') + ' ' + str(exc))
            return
        for key, value in values.items():
            self._color_swatches[key].configure(bg=value)
        self.colors_status.configure(text=self.tr('colors_saved'))

    def on_show(self):
        self.refresh()

    def _save(self):
        try:
            self.save_window_size(self.window_size_var.get())
        except (OSError, ValueError) as exc:
            self.status.configure(text=self.tr('error') + ' ' + str(exc))
            return
        self.status.configure(text=self.tr('saved'))


class ManualScreen(ttk.Frame):
    """Lazy, searchable, read-only extended help for the same 87 tooltip keys.

    Data comes only from bundled parameter_help JSON (cached by its loader).
    No timers, background tasks, file scans, writes or runtime side effects.
    """

    def __init__(self, master, language='pl', help_language=None, upstream_root_provider=None,
                 demo_root_provider=None):
        super().__init__(master, padding=16)
        self.language = language
        self.content_language = help_language or language
        self.keys = sorted(parameter_catalog())
        self.visible_keys = []
        self.current_key = None
        self.upstream_root_provider = upstream_root_provider or (lambda: canonical_roots()[0])
        self.demo_root_provider = demo_root_provider or (lambda: canonical_roots()[1])
        self._docs_view = None
        self._demo_view = None
        self._gui_docs_view = None
        self.title_label = ttk.Label(self, style='Heading.TLabel', text='Manual')
        self.title_label.pack(anchor='w', pady=(0, 10))
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill='both', expand=True)
        self.index_page = ttk.Frame(self.tabs)
        self.documentation_page = ttk.Frame(self.tabs)
        self.demo_documentation_page = ttk.Frame(self.tabs)
        self.gui_documentation_page = ttk.Frame(self.tabs)
        self.tabs.add(self.index_page, text='Index')
        self.tabs.add(self.documentation_page, text='Documentation')
        self.tabs.add(self.demo_documentation_page, text='Demo Project Documentation')
        self.tabs.add(self.gui_documentation_page, text='GUI Documentation')
        self.tabs.bind('<<NotebookTabChanged>>', self._tab_changed, add='+')
        self.search_var = tk.StringVar(self)
        bar = ttk.Frame(self.index_page)
        bar.pack(fill='x', pady=(0, 8))
        self.search_label = ttk.Label(bar)
        self.search_label.pack(side='left', padx=(0, 10))
        self.search_entry = ttk.Entry(bar, textvariable=self.search_var)
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_var.trace_add('write', self._search_changed)
        body = ttk.Panedwindow(self.index_page, orient='horizontal')
        body.pack(fill='both', expand=True)
        left = ttk.Frame(body)
        right = ttk.Frame(body)
        body.add(left, weight=1)
        body.add(right, weight=3)
        self.listbox = tk.Listbox(left, exportselection=False, font=('TkDefaultFont', 10),
                                  relief='flat', borderwidth=0, activestyle='none',
                                  background=COLORS['field'], foreground=COLORS['text'],
                                  selectbackground=COLORS['selection'],
                                  selectforeground=COLORS['accent_text'], highlightthickness=0)
        scroll_left = ttk.Scrollbar(left, orient='vertical', command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scroll_left.set)
        self.listbox.pack(side='left', fill='both', expand=True)
        scroll_left.pack(side='right', fill='y')
        self.listbox.bind('<<ListboxSelect>>', self._selected)
        self.details = tk.Text(right, wrap='word', state='disabled', relief='flat',
                               borderwidth=0, padx=18, pady=15,
                               font=('TkDefaultFont', 11),
                               background=COLORS['field'], foreground=COLORS['text'])
        scroll_right = ttk.Scrollbar(right, orient='vertical', command=self.details.yview)
        self.details.configure(yscrollcommand=scroll_right.set)
        self.details.pack(side='left', fill='both', expand=True)
        scroll_right.pack(side='right', fill='y')
        self.details.tag_configure('title', font=('TkDefaultFont', 14, 'bold'),
                                   foreground=COLORS['accent'], spacing3=14)
        self.details.tag_configure('head', font=('TkDefaultFont', 10, 'bold'),
                                  foreground=COLORS['muted'], spacing1=9, spacing3=4)
        self.details.tag_configure('body', spacing1=2, spacing3=12)
        self.details.tag_configure('option_value', font=('TkDefaultFont', 10, 'bold'),
                                   foreground=COLORS['success'], spacing1=9, spacing3=4)
        self.set_language(language, self.content_language)

    def _tab_changed(self, _event=None):
        """Construct and scan upstream documentation only on first opening."""
        selected = self.tabs.select()
        if selected == str(self.documentation_page):
            if self._docs_view is None:
                self._docs_view = UpstreamRstBrowser(self.documentation_page,
                                                      self.upstream_root_provider, self.language)
                self._docs_view.pack(fill='both', expand=True)
            else:
                self._docs_view.refresh_repository_if_changed()
        elif selected == str(self.demo_documentation_page):
            if self._demo_view is None:
                self._demo_view = DemoProjectDocsBrowser(self.demo_documentation_page,
                                                         self.demo_root_provider, self.language)
                self._demo_view.pack(fill='both', expand=True)
            else:
                self._demo_view.refresh_repository_if_changed()

        elif selected == str(self.gui_documentation_page):
            if self._gui_docs_view is None:
                self._gui_docs_view = GuiDocumentationBrowser(self.gui_documentation_page,
                                                               language=self.language)
                self._gui_docs_view.pack(fill='both', expand=True)

    def _record(self, key):
        return get_parameter_help(key, self.content_language)

    def _search_changed(self, *_args):
        self._filter()

    def _filter(self):
        query = self.search_var.get().strip().casefold()
        selected = self.current_key
        self.visible_keys = []
        for key in self.keys:
            record = self._record(key)
            searchable = [str(record.get(field, '')) for field in ('title', 'short', 'long', 'group', 'key')]
            if self.content_language == 'en':
                searchable.extend(choice['value']+' '+choice['description']
                                  for choice in record.get('options', []))
            if query and not any(query in value.casefold() for value in searchable):
                continue
            self.visible_keys.append(key)
        self.listbox.delete(0, 'end')
        for key in self.visible_keys:
            self.listbox.insert('end', self._record(key)['title'])
        if selected in self.visible_keys:
            idx = self.visible_keys.index(selected)
            self.listbox.selection_set(idx)
            self.listbox.see(idx)
        elif self.visible_keys:
            self.current_key = self.visible_keys[0]
            self.listbox.selection_set(0)
            self._render()
        else:
            self.current_key = None
            self._render()

    def _selected(self, _event=None):
        selection = self.listbox.curselection()
        if not selection or selection[0] >= len(self.visible_keys):
            return
        self.current_key = self.visible_keys[selection[0]]
        self._render()

    def show_parameter(self, key):
        self.tabs.select(self.index_page)
        if key not in parameter_catalog():
            raise KeyError('Unknown manual parameter: ' + str(key))
        self.search_var.set('')
        self.current_key = key
        self._filter()
        idx = self.visible_keys.index(key)
        self.listbox.selection_clear(0, 'end')
        self.listbox.selection_set(idx)
        self.listbox.see(idx)
        self._render()

    def _render(self):
        self.details.configure(state='normal')
        self.details.delete('1.0', 'end')
        if self.current_key is not None:
            record = self._record(self.current_key)
            self.details.insert('end', record['title'] + '\n', 'title')
            self.details.insert('end', record['short'] + '\n\n', 'body')
            self.details.insert('end', ('Opis rozszerzony' if self.content_language == 'pl'
                                        else 'Extended description') + '\n', 'head')
            self.details.insert('end', record['long'] + '\n\n', 'body')
            if self.content_language == 'en' and record.get('options'):
                self.details.insert('end', 'Available options\n', 'head')
                for choice in record['options']:
                    self.details.insert('end', choice['value'] + '\n', 'option_value')
                    self.details.insert('end', choice['description'] + '\n\n', 'body')
            self.details.insert('end', ('Identyfikator' if self.content_language == 'pl'
                                        else 'Parameter ID') + ': ' + self.current_key + '\n', 'head')
            self.details.insert('end', ('Dostępność' if self.content_language == 'pl'
                                        else 'Availability') + ': ' + record['status'] + '\n', 'body')
        self.details.configure(state='disabled')
        self.details.yview_moveto(0)

    def set_language(self, language, help_language=None):
        self.language = language
        self.content_language = help_language or language
        self.title_label.configure(text='Manual')
        self.tabs.tab(self.index_page, text='Index')
        self.tabs.tab(self.documentation_page, text='Documentation')
        self.tabs.tab(self.demo_documentation_page, text='Demo Project Documentation')
        self.tabs.tab(self.gui_documentation_page, text='GUI Documentation')
        if self._gui_docs_view is not None:
            self._gui_docs_view.set_language(language)
        if self._demo_view is not None:
            self._demo_view.set_language(language)
        if self._docs_view is not None:
            self._docs_view.set_language(language)
        self.search_label.configure(text='Szukaj:' if language == 'pl' else 'Search:')
        self._filter()
        self._render()
