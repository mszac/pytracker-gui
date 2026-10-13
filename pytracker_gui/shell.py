"""Small navigation shell. Experiment editor is a persistent independent view.

No timers, filesystem scans, extra processes or background threads are created
by navigation. Future screens are constructed at most once, on first selection.
"""
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from .app import PytrackerGUI
from .i18n import translate
from .screens import DashboardScreen, PlaceholderScreen, ManualScreen, GuiSettingsScreen
from .logs_screen import LogsHistoryScreen
from .storage import load_settings, save_settings, data_home
from .theme import apply_theme, brand_logo, icon, configure_saved_palette, valid_hex_color, COLORS, factory_palette

SCREEN_IDS = ('experiment', 'logs', 'statistics', 'manual', 'gui-settings')
SCREEN_TITLES = {
    'experiment': 'Eksperyment',
    'logs': 'Logi',
    'statistics': 'Statystyki',
    'manual': 'Podręcznik',
    'gui-settings': 'Ustawienia GUI',
}


class AppShell(ttk.Frame):
    """Owns only navigation and shared project label, not experiment behavior."""

    def __init__(self, master, *, home=None):
        # Read the existing palette parameters once at startup. No live repaint
        # or repeated processing while an experiment is running.
        configure_saved_palette(load_settings(Path(home) if home is not None else data_home()))
        apply_theme(master)
        super().__init__(master, padding=(7, 7, 7, 0), style='BrandLogo.TLabel')
        self.root = master
        self.pack(fill='both', expand=True)
        self.screen_id = tk.StringVar(master, value='experiment')
        self.project_context = tk.StringVar(master, value='')
        self.nav_buttons = {}
        self._screens = {}
        nav = ttk.Frame(self, style='BrandLogo.TLabel')
        nav.pack(fill='x', padx=4, pady=(0, 5))
        # Single round project logo: the old orange diamond is retired.
        self.brand_logo_label = ttk.Label(nav, image=brand_logo(self.root), style='BrandLogo.TLabel', cursor='hand2')
        self.brand_logo_label.pack(side='left', padx=(0, 5))
        self.brand_logo_label.bind('<Button-1>', lambda _event: self.open_home())
        self.brand_button = ttk.Button(nav, text='pytracker-gui', style='Brand.TButton',
                                       command=self.open_home, cursor='hand2')
        self.brand_button.pack(side='left', padx=(0, 15))
        for screen_id in SCREEN_IDS:
            button = ttk.Radiobutton(
                nav, variable=self.screen_id, value=screen_id,
                style='Toolbutton', command=lambda key=screen_id: self.select_screen(key))
            button.configure(image=icon(self.root, screen_id), compound='left')
            button.pack(side='left', padx=(0, 5))
            self.nav_buttons[screen_id] = button
        ttk.Label(nav, textvariable=self.project_context, style='ShellInfo.TLabel').pack(side='right', padx=8)
        ttk.Separator(self).pack(fill='x', pady=(0, 5))
        self.host = ttk.Frame(self, style='Shell.TFrame')
        self.host.pack(fill='both', expand=True)
        # Only Experiment is eagerly created because it is the initial view.
        # PytrackerGUI remains importable and testable as in previous releases.
        self.experiment = PytrackerGUI(self.host, home=home)
        self.experiment.on_language_change = self._language_changed
        self.experiment.on_manual_request = self.open_manual
        self._screens['experiment'] = self.experiment
        self.current_screen = 'experiment'
        self.experiment.project_name.trace_add('write', self._project_changed)
        self._project_changed()
        self._language_changed()
        self._update_nav_icons()
        # More room for the full demo list on normal displays; shrink on small screens.
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        preset = load_settings(self.experiment.home).get('window_size', '1429 × 1097')
        if preset not in GuiSettingsScreen.WINDOW_PRESETS:
            preset = '1429 × 1097'
        width, height = (int(x.strip()) for x in preset.split('×'))
        self.root.geometry(f'{min(width, max(940, screen_width - 90))}x'
                           f'{min(height, max(650, screen_height - 90))}')
        self.root.protocol('WM_DELETE_WINDOW', self.request_close)

    @property
    def created_screens(self):
        """Visible for tests; does not instantiate unopened screens."""
        return tuple(self._screens)

    def _update_nav_icons(self):
        for key, button in self.nav_buttons.items():
            button.configure(image=icon(self.root, key, active=(key == self.current_screen)))

    def _project_changed(self, *_args):
        self.project_context.set(
            translate('Projekt:', self.experiment.language_code) + ' ' + self.experiment.project_name.get())

    def _language_changed(self):
        lang = self.experiment.language_code
        for screen_id, button in self.nav_buttons.items():
            button.configure(text=translate(SCREEN_TITLES[screen_id], lang))
        self._project_changed()
        for key, screen in self._screens.items():
            if key == 'manual':
                screen.set_language(lang, self.experiment.help_language_code)
            elif key != 'experiment':
                screen.set_language(lang)

    def _gui_settings_snapshot(self):
        lang_map = {'pl': 'Polski', 'en': 'English'}
        is_pl = self.experiment.language_code == 'pl'
        return {
            'window_size': self.experiment.settings.get('window_size', '1429 × 1097'),
            'ICON_COLOR': self.experiment.settings.get('ICON_COLOR', factory_palette()['ICON_COLOR']),
            'COLORS': self.experiment.settings.get('COLORS', {}),
            'gui_home': str(self.experiment.home),
            'projects_root': str(self.experiment.project_root),
            'demo_root': self.experiment.demo_root.get().strip(),
            'upstream_root': self.experiment.upstream.get().strip(),
            'python': self.experiment.python.get().strip(),
            'language': lang_map.get(self.experiment.language_code, 'Polski'),
            'help_language': lang_map.get(self.experiment.help_language_code, 'Polski'),
            'auto_logs': ('Włączone' if is_pl else 'Enabled') if self.experiment.auto_show_logs.get()
                         else ('Wyłączone' if is_pl else 'Disabled'),
        }

    def _save_gui_window_size(self, choice):
        if choice not in GuiSettingsScreen.WINDOW_PRESETS:
            raise ValueError('Unsupported startup window size')
        # Reuse the existing settings file and the Experiment editor's in-memory
        # settings dictionary. Neither repository files nor YAML are touched.
        settings = dict(self.experiment.settings)
        settings['window_size'] = choice
        save_settings(self.experiment.home, settings)
        self.experiment.settings.update(settings)

    def _save_gui_colors(self, icon_color, colors):
        # Only existing theme.py identifiers are user-settable. Persist them
        # atomically in the same settings file as the window-size preference.
        if not valid_hex_color(icon_color):
            raise ValueError('Invalid ICON_COLOR')
        if not isinstance(colors, dict) or set(colors) != set(COLORS):
            raise ValueError('Invalid COLORS keys')
        if any(not valid_hex_color(value) for value in colors.values()):
            raise ValueError('Invalid COLORS value')
        settings = dict(self.experiment.settings)
        settings['ICON_COLOR'] = icon_color.upper()
        settings['COLORS'] = {key: colors[key].upper() for key in COLORS}
        save_settings(self.experiment.home, settings)
        self.experiment.settings.update(settings)

    def open_home(self):
        """Open the tile dashboard only on demand; same selection path as top nav."""
        self.select_screen('home')

    def select_screen(self, screen_id):
        """Switch only widget visibility; never commit/reset YAML or touch runner."""
        if screen_id not in SCREEN_IDS and screen_id != 'home':
            raise ValueError('Unknown screen: ' + str(screen_id))
        if screen_id == self.current_screen:
            self.screen_id.set(screen_id)
            return
        if screen_id not in self._screens:
            if screen_id == 'home':
                self._screens[screen_id] = DashboardScreen(
                    self.host, self.select_screen, self.experiment.language_code, self.root)
            elif screen_id == 'manual':
                self._screens[screen_id] = ManualScreen(
                    self.host, self.experiment.language_code, self.experiment.help_language_code,
                    upstream_root_provider=lambda: self.experiment.upstream.get(),
                    demo_root_provider=lambda: self.experiment.demo_root.get())
            elif screen_id == 'logs':
                self._screens[screen_id] = LogsHistoryScreen(
                    self.host, self.experiment.project_root, self.experiment.language_code)
            elif screen_id == 'gui-settings':
                self._screens[screen_id] = GuiSettingsScreen(
                    self.host, self._gui_settings_snapshot, self._save_gui_window_size,
                    self.experiment.language_code, save_colors=self._save_gui_colors,
                    on_gui_manual=self.open_gui_settings_manual)
            else:
                self._screens[screen_id] = PlaceholderScreen(
                    self.host, screen_id, self.experiment.language_code)
        self.experiment.info_popover.dismiss()
        self._screens[self.current_screen].pack_forget()
        self._screens[screen_id].pack(fill='both', expand=True)
        if screen_id in self._screens and hasattr(self._screens[screen_id], 'on_show'):
            self._screens[screen_id].on_show()
        self.current_screen = screen_id
        self.screen_id.set(screen_id)
        self._update_nav_icons()

    def open_gui_settings_manual(self, key):
        """Open the installed GUI Settings guide in the current interface language."""
        self.select_screen('manual')
        manual = self._screens['manual']
        manual.tabs.select(manual.gui_documentation_page)
        manual._gui_docs_view.select_file('docs/GUI_SETTINGS_HELP_V032_' +
                                          ('PL' if self.experiment.language_code == 'pl' else 'EN') + '.md')
        manual._gui_docs_view.show_topic(key)

    def open_manual(self, key):
        """Navigate directly to extended parameter help without editing any fields."""
        self.select_screen('manual')
        self._screens['manual'].show_parameter(key)

    def request_close(self):
        """Delegate all unsaved-edit and running-process safeguards unchanged."""
        return self.experiment.request_close()
