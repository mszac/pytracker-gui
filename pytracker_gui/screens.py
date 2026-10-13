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
from .help_widgets import InfoButton, InfoPopover


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
        'gui_home': 'Katalog danych GUI', 'projects_root': 'Katalog projektów i historii uruchomień',
        'demo_root': 'Repozytorium projektów startowych', 'upstream_root': 'Oryginalne repozytorium',
        'python': 'Interpreter Python',
        'path_hint': 'Ścieżki są tutaj tylko do odczytu. Obsługiwane ścieżki repozytoriów można zmienić w Eksperyment → Środowisko.',
        'language': 'Język interfejsu', 'help_language': 'Język podpowiedzi',
        'auto_logs': 'Automatyczne otwieranie logów', 'journal': 'Dziennik konsoli',
        'journal_value': 'Jeden log narastający · .log / .log.part',
        'saved': 'Rozmiar zapisany. Zostanie użyty przy następnym uruchomieniu.',
        'error': 'Nie udało się zapisać ustawień:',
        'colors': 'Kolory interfejsu',
        'colors_hint': 'Edytuj istniejące wartości ICON_COLOR i COLORS w formacie #RRGGBB. Zapisz kolory i uruchom ponownie GUI, aby zastosować zmiany.',
        'save_colors': 'Zapisz kolory', 'reset_colors': 'Przywróć domyślne wartości',
        'colors_saved': 'Kolory zapisane. Uruchom GUI ponownie, aby je zastosować.',
        'colors_error': 'Nieprawidłowa wartość #RRGGBB dla:',
    },
    'en': {
        'subtitle': 'Application settings and GUI paths · separate from experiment configuration',
        'window': 'Window & appearance', 'paths': 'Paths & environment', 'preferences': 'Preferences',
        'window_size': 'Startup window size', 'save': 'Save window size',
        'window_hint': 'Saved size takes effect at the next launch; smaller displays may limit the actual window size.',
        'tile_size': 'Home dashboard tiles', 'tile_value': '546 × 365 px · fixed size',
        'gui_home': 'GUI data directory', 'projects_root': 'Project history',
        'demo_root': 'Demo repository', 'upstream_root': 'Original upstream repository',
        'python': 'Python interpreter',
        'path_hint': 'These paths are read-only here. Edit supported repository paths in Experiment → Environment.',
        'language': 'Interface language', 'help_language': 'Tooltip language',
        'auto_logs': 'Automatically open Logs', 'journal': 'Console journal',
        'journal_value': 'Single incremental log · .log / .log.part',
        'saved': 'Startup size saved. It will apply on the next launch.',
        'error': 'Could not save settings:',
        'colors': 'Interface colors',
        'colors_hint': 'Edit existing ICON_COLOR and COLORS values using #RRGGBB. Save, then restart the GUI to apply.',
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
        # Compatibility metadata: the visible home title is rendered in the header.
        self.title_label = ttk.Label(self, style='DashboardTitle.TLabel')
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
        assets = Path(__file__).with_name('assets')
        master_root = root or self.winfo_toplevel()
        # Static 1128px-wide header shares the fixed tile board's coordinate space.
        # Draw the title natively; keep only the logo as a small pre-scaled PNG.
        header = tk.Frame(board, height=102, width=1128, bg=COLORS['surface'])
        header.grid(row=0, column=0, columnspan=2, sticky='w')
        header.grid_propagate(False)
        header_canvas = tk.Canvas(header, width=1128, height=102, bg=COLORS['surface'],
                                  bd=0, highlightthickness=0)
        header_canvas.pack()
        from tkinter import font as tkfont
        family = ttk.Style(self).lookup('Brand.TButton', 'font')
        try:
            brand_family = tkfont.Font(root=self, font=family).actual('family')
        except tk.TclError:
            brand_family = 'TkDefaultFont'
        self._header_font = tkfont.Font(root=self, family=brand_family, size=30, weight='bold')
        header_canvas.create_text(564, 51, text='pytracker-gui', fill=COLORS['text'],
                                  font=self._header_font, anchor='center')
        self._header_logo = tk.PhotoImage(master=master_root,
                                          file=str(assets / 'dashboard-brand-logo.png'))
        if (self._header_logo.width(), self._header_logo.height()) != (96, 96):
            raise ValueError('Incorrect dashboard brand logo size')
        header_canvas.create_image(1128, 3, image=self._header_logo, anchor='ne')
        self.header = header
        self.header_canvas = header_canvas
        # No grid weights or sticky='nsew': an enlarged window leaves free space,
        # and a smaller window cannot stretch or compress any of the four tiles.
        style = ttk.Style(self)
        style.configure('DashboardImage.TButton', padding=0, borderwidth=0,
                        relief='flat', background=COLORS['surface_alt'])
        # The image is the entire button surface, not an inset of a themed border.
        style.layout('DashboardImage.TButton', [('Button.label', {'sticky': 'nswe'})])
        self.tile_buttons = {}
        self._tile_images = {}
        for index, (screen_id, _, _) in enumerate(self.TILES):
            image = tk.PhotoImage(master=master_root, file=str(assets / f'dashboard-{screen_id}.png'))
            if (image.width(), image.height()) != self.TILE_SIZE:
                raise ValueError('Incorrect dashboard tile image size: ' + screen_id)
            self._tile_images[screen_id] = image
            tile = ttk.Button(board, style='DashboardImage.TButton',
                              image=image, compound='none', cursor='hand2',
                              command=lambda key=screen_id: self.on_select(key))
            tile.grid(row=1 + index // 2, column=index % 2, padx=9, pady=9)
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


GUI_HELP_SHORT = {'window': 'Window-size and tile information; the window preset is saved for the next launch.', 'window_size': 'Choose a startup-size preset. The usable display area may limit it.', 'save': 'Save the selected window preset for the next application launch.', 'tile_size': 'The four Home images remain 546 × 365 pixels; resizing does not rescale them.', 'paths': 'These paths are displayed for reference; editable repository paths are in Experiment → Environment.', 'gui_home': 'Application-owned settings and state directory; not a measurement-output folder.', 'projects_root': 'Directory containing GUI projects, profiles, and run histories.', 'demo_root': 'Root of the starter-project examples repository.', 'upstream_root': 'Root of the original tobii-pytracker source repository.', 'python': 'Configured interpreter used to launch experiments; this field is read-only here.', 'preferences': 'Current application preferences, displayed here without edit controls.', 'language': 'Language currently used for interface labels.', 'help_language': 'Language currently selected for experiment parameter help.', 'auto_logs': 'Shows whether the live Logs view opens automatically during a run.', 'journal': 'Each run has a bounded, incrementally written console journal (.log or .log.part).', 'colors': 'Edit the existing theme palette with six-digit RGB values (#RRGGBB).', 'save_colors': 'Validate and save the entire palette. Restart to apply the saved colors.', 'reset_colors': 'Load factory colors into the editor; press Save colors to keep them.', 'ICON_COLOR': 'Color applied to supported inactive UI icons; selected icons may use other colors.'}
GUI_HELP_TITLES = {key: GUI_SETTINGS_TEXTS["en"].get(key, key) for key in GUI_HELP_SHORT}
GUI_COLOR_ROLES = {'window': 'Main application window background.', 'surface': 'Background of primary content panels.', 'surface_alt': 'Secondary panel and popover background.', 'field': 'Input fields and inset content areas.', 'hover': 'Hover-state background where the theme supports it.', 'border': 'Panel and control outlines.', 'text': 'Primary text.', 'muted': 'Secondary and less prominent text.', 'accent': 'Primary orange accent for emphasis and selected controls.', 'accent_hover': 'Hover shade of the accent color.', 'accent_text': 'Text drawn on an accent-colored background.', 'selection': 'Selection highlight in supported controls.', 'success': 'Positive status indicators.'}
for _gui_color in COLORS:
    GUI_HELP_SHORT.setdefault(_gui_color, GUI_COLOR_ROLES[_gui_color] + " Enter #RRGGBB; save and restart to apply.")
    GUI_HELP_TITLES.setdefault(_gui_color, _gui_color)

GUI_HELP_SHORT_PL = {'window': 'Informacje o rozmiarze okna i kafelkach. Wybrany rozmiar okna zostanie użyty przy następnym uruchomieniu.', 'window_size': 'Wybierz początkowy rozmiar okna. Obszar roboczy mniejszego ekranu może go ograniczyć.', 'save': 'Zapisz wybrany rozmiar okna do zastosowania przy następnym uruchomieniu aplikacji.', 'tile_size': 'Cztery obrazy kafelków panelu głównego zachowują rozmiar 546 × 365 pikseli. Zmiana rozmiaru okna ich nie skaluje.', 'paths': 'Ścieżki służą tutaj tylko do odczytu. Obsługiwane ścieżki repozytoriów zmienisz w Eksperyment → Środowisko.', 'gui_home': 'Katalog ustawień i stanu aplikacji GUI, a nie katalog z wynikami pomiarów.', 'projects_root': 'Katalog projektów użytkownika, profili i historii uruchomień.', 'demo_root': 'Katalog główny repozytorium dostarczonych projektów startowych.', 'upstream_root': 'Katalog główny oryginalnego repozytorium tobii-pytracker.', 'python': 'Interpreter używany do uruchamiania eksperymentów. Tutaj ścieżka jest tylko do odczytu.', 'preferences': 'Bieżące preferencje aplikacji wyświetlane bez możliwości edycji na tej stronie.', 'language': 'Język etykiet i menu interfejsu aplikacji.', 'help_language': 'Język opisów parametrów eksperymentu i odpowiadającego im manuala.', 'auto_logs': 'Informuje, czy podgląd logów otwiera się automatycznie podczas uruchomienia eksperymentu.', 'journal': 'Każde uruchomienie ma jeden narastający dziennik konsoli (.log lub .log.part) z ograniczonym buforem.', 'colors': 'Zmieniaj istniejącą paletę GUI, podając sześciocyfrowe wartości RGB (#RRGGBB).', 'save_colors': 'Sprawdź i zapisz całą paletę. Zapisane kolory zostaną zastosowane po ponownym uruchomieniu GUI.', 'reset_colors': 'Wczytaj kolory fabryczne do edytora. Aby je zachować, wybierz Zapisz kolory.', 'ICON_COLOR': 'Kolor obsługiwanych nieaktywnych ikon GUI. Ikony zaznaczonych sekcji mogą używać innych kolorów.'}
GUI_COLOR_ROLES_PL = {'window': 'Tło głównego okna aplikacji.', 'surface': 'Tło głównych paneli treści.', 'surface_alt': 'Tło paneli pomocniczych i okienek podpowiedzi.', 'field': 'Tło pól wejściowych i zagłębionych obszarów treści.', 'hover': 'Tło po najechaniu kursorem w obsługiwanych kontrolkach.', 'border': 'Obramowania paneli i kontrolek.', 'text': 'Podstawowy kolor tekstu.', 'muted': 'Tekst drugoplanowy i mniej wyróżniony.', 'accent': 'Główny pomarańczowy akcent dla wyróżnień i zaznaczonych kontrolek.', 'accent_hover': 'Odcień akcentu po najechaniu kursorem.', 'accent_text': 'Tekst wyświetlany na tle w kolorze akcentu.', 'selection': 'Podświetlenie zaznaczenia w obsługiwanych kontrolkach.', 'success': 'Wskaźniki pozytywnego statusu.'}
for _gui_color_pl in COLORS:
    GUI_HELP_SHORT_PL.setdefault(_gui_color_pl, GUI_COLOR_ROLES_PL[_gui_color_pl] + " Wpisz #RRGGBB, zapisz kolory i uruchom ponownie GUI.")

class GuiSettingsScreen(ttk.Frame):
    """Lightweight GUI settings view; never edits experiment YAML or repository data."""

    WINDOW_PRESETS = ('940 × 650', '1100 × 800', '1300 × 960', '1429 × 1097', '1600 × 1000')

    def __init__(self, master, settings_provider, save_window_size, language='pl', save_colors=None, on_gui_manual=None):
        super().__init__(master, padding=(15, 12))
        self.settings_provider = settings_provider
        self.save_window_size = save_window_size
        self.save_colors = save_colors
        self.on_gui_manual = on_gui_manual
        self._info_popover = InfoPopover(self.winfo_toplevel(), self._gui_help_record, self._open_gui_manual)
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
        self.title = ttk.Label(self, style='GuiSettingsTitle.TLabel', text='Ustawienia GUI' if self.language == 'pl' else 'GUI Settings')
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
        self._caption(control, 'window_size').pack(side='left', padx=(0, 4))
        self._info(control, 'window_size').pack(side='left', padx=(0, 12))
        self.preset_combo = ttk.Combobox(control, textvariable=self.window_size_var,
                                          state='readonly', width=17, values=self.WINDOW_PRESETS)
        self.preset_combo.pack(side='left', padx=(0, 12))
        self.save_button = ttk.Button(control, text=self.tr('save'), command=self._save)
        self.save_button.pack(side='left')
        self._info(control, 'save').pack(side='left', padx=(7, 0))
        self.status = ttk.Label(self.window_card, text='', style='GuiSettingsSubtitle.TLabel')
        self.status.pack(anchor='w', padx=15, pady=(0, 5))
        self.window_hint = self._hint(self.window_card, 'window_hint')
        self.window_hint.pack(anchor='w', padx=15, pady=(0, 10))
        tiles = tk.Frame(self.window_card, bg=COLORS['field'])
        tiles.pack(fill='x', padx=15, pady=(0, 12))
        self._caption(tiles, 'tile_size').pack(side='left', padx=(0, 5))
        self._info(tiles, 'tile_size').pack(side='left')
        self.tile_value = tk.Label(tiles, text=self.tr('tile_value'), bg=COLORS['field'],
                                   fg=COLORS['text'], font=('Segoe UI', 10))
        self.tile_value.pack(side='left', padx=(20, 0))

        self.paths_card = self._card('paths')
        for key in ('gui_home', 'projects_root', 'demo_root', 'upstream_root', 'python'):
            line = tk.Frame(self.paths_card, bg=COLORS['field'])
            line.pack(fill='x', padx=15, pady=(0, 8))
            self._caption(line, key, width=25).pack(side='left', padx=(0, 5))
            self._info(line, key).pack(side='left', padx=(0, 9))
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
            self._caption(line, key, width=25).pack(side='left', padx=(0, 5))
            self._info(line, key).pack(side='left', padx=(0, 9))
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
            self._info(line, key).pack(side='left', padx=(0, 3))
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
        self.save_colors_button.pack(side='left', padx=(0, 4))
        self._info(actions, 'save_colors').pack(side='left', padx=(0, 10))
        self.reset_colors_button = ttk.Button(actions, text=self.tr('reset_colors'),
                                              command=self._reset_colors)
        self.reset_colors_button.pack(side='left')
        self._info(actions, 'reset_colors').pack(side='left', padx=(7, 0))
        self.colors_status = ttk.Label(self.colors_card, style='GuiSettingsSubtitle.TLabel')
        self.colors_status.pack(anchor='w', padx=15, pady=(0, 9))
        self._bind_section_wheel()

    def _gui_help_record(self, key):
        catalog = GUI_HELP_SHORT_PL if self.language == 'pl' else GUI_HELP_SHORT
        title = (GUI_SETTINGS_TEXTS['pl'].get(key, key) if self.language == 'pl'
                 else GUI_HELP_TITLES.get(key, key))
        return {'title': title, 'short': catalog.get(key,
                'Kolor interfejsu GUI. Wpisz #RRGGBB i uruchom ponownie GUI.' if self.language == 'pl'
                else 'GUI appearance color. Enter a #RRGGBB value; restart to apply.')}

    def _info(self, parent, key):
        return InfoButton(parent, help_key=key, callback=self._info_popover.toggle)

    def _open_gui_manual(self, key):
        if self.on_gui_manual is not None:
            self.on_gui_manual(key)

    def _bind_section_wheel(self):
        # A page-local bindtag reaches nested labels, frames, entries and buttons
        # without a global wheel handler or modifying their other bindings.
        tag = 'GuiSettingsWheel_' + str(id(self))

        def attach(widget):
            widget.bindtags((tag,) + tuple(t for t in widget.bindtags() if t != tag))
            for child in widget.winfo_children():
                attach(child)

        attach(self)
        self.bind_class(tag, '<MouseWheel>', self._scroll_wheel)
        self.bind_class(tag, '<Button-4>', self._scroll_wheel)
        self.bind_class(tag, '<Button-5>', self._scroll_wheel)

    def _scroll_wheel(self, event):
        if event.num == 4:
            steps = -1
        elif event.num == 5:
            steps = 1
        else:
            delta = event.delta
            if not delta:
                return
            # Windows emits multiples of 120; macOS can emit smaller deltas.
            steps = -int(delta / 120) if abs(delta) >= 120 else (-1 if delta > 0 else 1)
        self.settings_canvas.yview_scroll(steps, 'units')
        return 'break'

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
        self.title.configure(text='Ustawienia GUI' if self.language == 'pl' else 'GUI Settings')
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


# Polish presentation titles in Manual → Index only; JSON and rendered manuals stay unchanged.
POLISH_INDEX_TITLES = {'gui.demo_root': 'Katalog projektów demonstracyjnych', 'gui.upstream_root': 'Katalog repozytorium źródłowego', 'gui.gaze': 'Źródło danych o spojrzeniu', 'dataset.image.bbox_model': 'Model obszarów obrazu', 'dataset.text.bbox_model': 'Model obszarów tekstu', 'dataset.time_series.bbox_model': 'Model obszarów szeregu czasowego', 'dataset.text.font_height': 'Wysokość czcionki tekstu', 'runtime.enable_voice': 'Rejestrowanie głosu / --enable_voice', 'runtime.raw_data': 'Dane surowe / --raw_data', 'runtime.log_level': 'Poziom rejestrowania / --log_level', 'iohub.mouse.name': 'Nazwa urządzenia MouseGaze', 'iohub.mouse.auto_report_events': 'Automatyczne zgłaszanie zdarzeń MouseGaze', 'iohub.common.save_events': 'Zapisywanie zdarzeń', 'iohub.common.stream_events': 'Strumieniowanie zdarzeń', 'iohub.common.event_buffer_length': 'Pojemność bufora zdarzeń', 'iohub.common.monitor_event_types': 'Monitorowane typy zdarzeń', 'iohub.calibration.enable': 'Włączenie kalibracji', 'iohub.calibration.type': 'Typ kalibracji', 'iohub.calibration.randomize': 'Losowa kolejność celów kalibracji', 'iohub.calibration.auto_pace': 'Automatyczne tempo kalibracji', 'iohub.calibration.pacing_speed': 'Szybkość kalibracji', 'iohub.calibration.screen_background_color': 'Kolor tła kalibracji', 'iohub.calibration.target_type': 'Typ celu kalibracyjnego', 'iohub.calibration.color_type': 'Typ zapisu koloru', 'iohub.calibration.unit_type': 'Jednostki wymiarów', 'iohub.calibration.target_attributes.outer_diameter': 'Średnica zewnętrzna celu', 'iohub.calibration.target_attributes.outer_stroke_width': 'Grubość zewnętrznego obrysu', 'iohub.calibration.target_attributes.outer_fill_color': 'Kolor wypełnienia zewnętrznego', 'iohub.calibration.target_attributes.outer_line_color': 'Kolor zewnętrznego obrysu', 'iohub.calibration.target_attributes.inner_diameter': 'Średnica wewnętrzna celu', 'iohub.calibration.target_attributes.inner_stroke_width': 'Grubość wewnętrznego obrysu', 'iohub.calibration.target_attributes.inner_fill_color': 'Kolor wypełnienia wewnętrznego', 'iohub.calibration.target_attributes.inner_line_color': 'Kolor wewnętrznego obrysu', 'iohub.calibration.target_attributes.animate.enable': 'Włączenie animacji celu', 'iohub.calibration.target_attributes.animate.movement_velocity': 'Prędkość ruchu celu', 'iohub.calibration.target_attributes.animate.expansion_ratio': 'Współczynnik powiększenia celu', 'iohub.calibration.target_attributes.animate.expansion_speed': 'Szybkość powiększania celu', 'iohub.calibration.target_attributes.animate.contract_only': 'Tylko zmniejszanie celu', 'iohub.runtime_settings.sampling_rate': 'Częstotliwość próbkowania', 'iohub.runtime_settings.track_eyes': 'Śledzone oczy', 'iohub.controls.move': 'Sterowanie ruchem MouseGaze', 'iohub.controls.blink': 'Symulacja mrugnięcia MouseGaze', 'iohub.controls.saccade_threshold': 'Próg sakkady', 'iohub.tobii.enable': 'Włączenie urządzenia Tobii', 'iohub.tobii.model_name': 'Nazwa modelu Tobii', 'iohub.tobii.serial_number': 'Numer seryjny Tobii', 'iohub.tobii.manufacturer_name': 'Nazwa producenta Tobii', 'bbox_model.folder': 'Katalog własnego modelu obszarów', 'bbox_model.module': 'Moduł własnego modelu obszarów', 'bbox_model.class': 'Klasa własnego modelu obszarów'}

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
        record = get_parameter_help(key, self.content_language)
        if self.content_language == 'pl' and key in POLISH_INDEX_TITLES:
            return {**record, 'title': POLISH_INDEX_TITLES[key]}
        return record

    def _search_changed(self, *_args):
        self._filter()

    def _filter(self):
        query = self.search_var.get().strip().casefold()
        selected = self.current_key
        self.visible_keys = []
        for key in self.keys:
            record = self._record(key)
            searchable = [str(record.get(field, '')) for field in ('title', 'short', 'long', 'group', 'key')]
            if record.get('options'):
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
            if record.get('options'):
                self.details.insert('end', ('Dostępne wartości\n' if self.content_language == 'pl' else 'Available options\n'), 'head')
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
        self.title_label.configure(text='Podręcznik' if language == 'pl' else 'Manual')
        self.tabs.tab(self.index_page, text='Indeks' if language == 'pl' else 'Index')
        self.tabs.tab(self.documentation_page, text='Dokumentacja' if language == 'pl' else 'Documentation')
        self.tabs.tab(self.demo_documentation_page, text='Dokumentacja projektów demonstracyjnych' if language == 'pl' else 'Demo Project Documentation')
        self.tabs.tab(self.gui_documentation_page, text='Dokumentacja GUI' if language == 'pl' else 'GUI Documentation')
        if self._gui_docs_view is not None:
            self._gui_docs_view.set_language(language)
        if self._demo_view is not None:
            self._demo_view.set_language(language)
        if self._docs_view is not None:
            self._docs_view.set_language(language)
        self.search_label.configure(text='Szukaj:' if language == 'pl' else 'Search:')
        self._filter()
        self._render()
