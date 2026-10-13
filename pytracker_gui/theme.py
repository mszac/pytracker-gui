"""Static charcoal/orange ttk appearance; native Tk only, no additional runtime packages.

No timers, image re-rasterization, font downloads, or event loops. Tiny PNG
icons are packaged with the GUI and loaded once per Tk root.
"""
from pathlib import Path
import base64
import json
import struct
import zlib
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

COLORS = {
    'window': '#11171e',
    'surface': '#1c252e',
    'surface_alt': '#222d38',
    'field': '#161e26',
    'hover': '#303d49',
    'border': '#394754',
    'text': '#f2f5f9',
    'muted': '#adbdcc',
    'accent': '#ff9d45',
    'accent_hover': '#ffb775',
    'accent_text': '#131820',
    'selection': '#ff8931',
    'success': '#72d46a',
}

_ASSETS = Path(__file__).with_name('assets')
# Independent icon-only color parameter. It can later be exposed in GUI Settings;
# orange selection text, button fill, highlight and brand artwork remain untouched.
ICON_COLOR = '#22289B'  # unselected icons: RGB(34, 40, 155)
_FACTORY_COLORS = dict(COLORS)  # existing palette defaults, for safe reset
_FACTORY_ICON_COLOR = ICON_COLOR
_ICON_ALPHA_MASKS = None


def valid_hex_color(value):
    """Strict #RRGGBB validation for existing theme values."""
    return (isinstance(value, str) and len(value) == 7 and value[0] == '#' and
            all(ch in '0123456789abcdefABCDEF' for ch in value[1:]))


def factory_palette():
    """Return existing default palette values; no extra user-visible parameters."""
    return {'ICON_COLOR': _FACTORY_ICON_COLOR, 'COLORS': dict(_FACTORY_COLORS)}


def configure_saved_palette(settings):
    """Apply saved overrides once, before first widget/theme construction.

    Ignore corrupt, unknown or invalid values; never allocate images here.
    Mutate COLORS in place because other GUI modules already reference it.
    """
    global ICON_COLOR
    COLORS.clear()
    COLORS.update(_FACTORY_COLORS)
    ICON_COLOR = _FACTORY_ICON_COLOR
    if not isinstance(settings, dict):
        return
    color = settings.get('ICON_COLOR')
    if valid_hex_color(color):
        ICON_COLOR = color.upper()
    saved = settings.get('COLORS')
    if isinstance(saved, dict):
        for key, value in saved.items():
            if key in _FACTORY_COLORS and valid_hex_color(value):
                COLORS[key] = value.upper()



def _icon_masks():
    """Load small precomputed anti-aliased alpha masks on first icon use."""
    global _ICON_ALPHA_MASKS
    if _ICON_ALPHA_MASKS is None:
        _ICON_ALPHA_MASKS = json.loads((_ASSETS / 'icon-alpha-masks.json').read_text(encoding='utf-8'))
    return _ICON_ALPHA_MASKS


def _png_chunk(name, payload):
    return (struct.pack('>I', len(payload)) + name + payload +
            struct.pack('>I', zlib.crc32(name + payload) & 0xffffffff))


def _tinted_icon(root, name, color):
    """Build a 40px RGBA image from a cached alpha mask with stdlib only.

    Work is performed once per name/color per Tk root, not during redraws or
    window resizing. Source icon geometry and antialiasing stay unchanged.
    """
    if (not isinstance(color, str) or len(color) != 7 or color[0] != '#' or
            any(ch not in '0123456789abcdefABCDEF' for ch in color[1:])):
        raise ValueError('ICON_COLOR must be #RRGGBB')
    mask = _icon_masks()[name]
    width, height = mask['w'], mask['h']
    alpha = zlib.decompress(base64.b64decode(mask['alpha']))
    if len(alpha) != width * height:
        raise ValueError('Invalid icon alpha mask: ' + name)
    rgb = bytes.fromhex(color[1:])
    row_pixels = []
    for y in range(height):
        arow = alpha[y * width:(y + 1) * width]
        row_pixels.append(b'\x00' + b''.join(rgb + bytes((a,)) for a in arow))
    png = (b'\x89PNG\r\n\x1a\n' +
           _png_chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)) +
           _png_chunk(b'IDAT', zlib.compress(b''.join(row_pixels), 6)) +
           _png_chunk(b'IEND', b''))
    return tk.PhotoImage(master=root, data=base64.b64encode(png), format='png')


def apply_theme(root):
    """Install one fixed native ttk palette; the UI does not poll or restyle."""
    if getattr(root, '_pytracker_dark_theme', False):
        return
    c = COLORS
    style = ttk.Style(root)
    families = set(tkfont.families(root))
    family = 'Segoe UI' if 'Segoe UI' in families else ('DejaVu Sans' if 'DejaVu Sans' in families else 'TkDefaultFont')
    if 'clam' in style.theme_names():
        style.theme_use('clam')
    root.configure(background=c['window'])
    root.option_add('*Font', 'TkDefaultFont')
    root.option_add('*TCombobox*Listbox.background', c['field'])
    root.option_add('*TCombobox*Listbox.foreground', c['text'])
    root.option_add('*TCombobox*Listbox.selectBackground', c['selection'])
    root.option_add('*TCombobox*Listbox.selectForeground', c['accent_text'])
    root.option_add('*TCombobox*Listbox.font', 'TkDefaultFont')

    style.configure('.', background=c['surface'], foreground=c['text'], font=(family, 10))
    style.configure('TFrame', background=c['surface'])
    style.configure('Shell.TFrame', background=c['window'])
    style.configure('ShellTitle.TLabel', background=c['window'], foreground=c['text'], font=(family, 12, 'bold'))
    style.configure('BrandIcon.TLabel', background=c['window'], foreground=c['accent'],
                    font=(family, 19, 'bold'))
    style.configure('Brand.TButton', background=c['window'], foreground=c['text'],
                    padding=(0, 0), borderwidth=0, relief='flat', font=(family, 17, 'bold'))
    style.map('Brand.TButton', background=[('user1', c['hover']), ('active', c['window']), ('pressed', c['window'])],
              foreground=[('user1', c['accent']), ('active', c['accent']), ('pressed', c['accent'])])
    style.configure('DashboardTitle.TLabel', background=c['surface'], foreground=c['text'],
                    font=(family, 17, 'bold'))
    style.configure('Dashboard.TButton', background=c['surface_alt'], foreground=c['text'],
                    borderwidth=1, bordercolor=c['border'], padding=(24, 30),
                    relief='flat', font=(family, 13, 'bold'))
    style.map('Dashboard.TButton', background=[('active', c['hover']), ('pressed', c['surface'])],
              foreground=[('active', c['accent'])], bordercolor=[('active', c['accent'])])
    style.configure('ShellInfo.TLabel', background=c['window'], foreground=c['muted'])
    style.configure('BrandLogo.TLabel', background=c['window'])
    style.configure('TLabel', background=c['surface'], foreground=c['text'])
    style.configure('Title.TLabel', background=c['surface'], foreground=c['text'], font=(family, 16, 'bold'))
    style.configure('Heading.TLabel', background=c['surface'], foreground=c['text'], font=(family, 11, 'bold'))
    style.configure('Muted.TLabel', background=c['surface'], foreground=c['muted'])
    style.configure('TLabelframe', background=c['surface'], borderwidth=1,
                    relief='solid', bordercolor=c['border'], padding=6)
    style.configure('TLabelframe.Label', background=c['surface'], foreground=c['text'],
                    font=('TkDefaultFont', 10, 'bold'), padding=(4, 2))
    style.configure('TSeparator', background=c['border'])
    style.configure('TButton', background=c['surface_alt'], foreground=c['text'],
                    padding=(11, 7), borderwidth=1, bordercolor=c['border'],
                    relief='flat', focusthickness=0)
    style.map('TButton', background=[('disabled', c['surface']), ('user1', c['accent_hover']), ('pressed', c['hover']), ('active', c['hover'])],
              foreground=[('disabled', c['muted']), ('active', c['text'])],
              bordercolor=[('user1', c['accent']), ('active', c['accent'])])
    style.configure('Accent.TButton', background=c['accent'], foreground=c['accent_text'],
                    padding=(12, 8), borderwidth=1, bordercolor=c['accent'],
                    relief='flat', font=('TkDefaultFont', 10, 'bold'))
    style.map('Accent.TButton', background=[('disabled', c['hover']), ('user1', c['selection']), ('pressed', c['selection']), ('active', c['accent_hover'])],
              foreground=[('disabled', c['muted']), ('active', c['accent_text'])])
    style.configure('TEntry', fieldbackground=c['field'], foreground=c['text'],
                    insertcolor=c['text'], padding=(9, 7), borderwidth=1,
                    bordercolor=c['border'], lightcolor=c['border'], darkcolor=c['border'])
    style.map('TEntry', bordercolor=[('focus', c['accent']), ('disabled', c['border'])],
              fieldbackground=[('readonly', c['surface_alt']), ('disabled', c['surface'])],
              foreground=[('disabled', c['muted'])])
    style.configure('TCombobox', fieldbackground=c['field'], background=c['surface_alt'],
                    foreground=c['text'], arrowcolor=c['muted'], padding=(7, 6),
                    bordercolor=c['border'], lightcolor=c['border'], darkcolor=c['border'])
    style.map('TCombobox', fieldbackground=[('readonly', c['field']), ('disabled', c['surface'])],
              foreground=[('readonly', c['text']), ('disabled', c['muted'])],
              background=[('active', c['hover'])], arrowcolor=[('active', c['accent'])],
              bordercolor=[('focus', c['accent'])])
    style.configure('TRadiobutton', background=c['surface'], foreground=c['text'], padding=(3, 4),
                    indicatorcolor=c['field'], indicatormargin=3)
    style.map('TRadiobutton', background=[('active', c['surface'])],
              foreground=[('disabled', c['muted'])],
              indicatorcolor=[('selected', c['accent']), ('active', c['accent_hover'])])
    style.configure('TCheckbutton', background=c['surface'], foreground=c['text'], padding=(3, 4),
                    indicatorcolor=c['field'])
    style.map('TCheckbutton', background=[('active', c['surface'])],
              indicatorcolor=[('selected', c['accent']), ('active', c['accent_hover'])])
    style.configure('TNotebook', background=c['surface'], bordercolor=c['border'],
                    borderwidth=0, tabmargins=(0, 0, 0, 1))
    style.configure('TNotebook.Tab', background=c['surface_alt'], foreground=c['muted'],
                    padding=(12, 9), borderwidth=0, font=(family, 10))
    style.map('TNotebook.Tab', background=[('selected', c['surface']), ('active', c['hover'])],
              foreground=[('selected', c['accent']), ('active', c['text'])],
              padding=[('selected', (6, 9))])  # 50% of the previous 12px horizontal inset
    style.configure('TScrollbar', background=c['surface_alt'], troughcolor=c['field'],
                    arrowcolor=c['muted'], bordercolor=c['surface'], width=12)
    style.map('TScrollbar', background=[('active', c['hover']), ('pressed', c['accent'])])
    style.configure('TTreeview', background=c['field'], fieldbackground=c['field'],
                    foreground=c['text'], rowheight=27, bordercolor=c['border'])
    style.map('TTreeview', background=[('selected', c['selection'])],
              foreground=[('selected', c['accent_text'])])
    style.configure('Toolbutton', background=c['window'], foreground=c['muted'], padding=(12, 10),
                    borderwidth=0, relief='flat', font=('TkDefaultFont', 10, 'bold'))
    style.map('Toolbutton', background=[('selected', c['surface_alt']), ('active', c['surface_alt'])],
              foreground=[('selected', c['accent']), ('active', c['text'])])
    _install_transient_control_feedback(root)
    root._pytracker_dark_theme = True


def _install_transient_control_feedback(root):
    """Paint the cue on mouse press, before ttk invokes the command on release.

    One idle redraw and one bounded timer per click; no action delay or polling.
    Editable controls and persistent navigation state remain unchanged.
    """
    def clear_focus():
        try:
            grabbed = root.grab_current()
            if grabbed is None or grabbed is root:
                root.focus_set()
        except tk.TclError:
            pass

    def press(event):
        widget = event.widget
        if widget.winfo_toplevel() is not root or widget.winfo_class() != 'TButton':
            return
        style_name = str(widget.cget('style'))
        if style_name in ('DashboardImage.TButton', 'LogsAccent.TButton'):
            return
        if widget.instate(('disabled',)):
            return
        try:
            widget.state(['user1'])
            # Flush only pending idle drawing work. Do not process events or
            # postpone the native ttk release/command handler.
            widget.update_idletasks()
        except tk.TclError:
            return

        def end_flash():
            try:
                if widget.winfo_exists():
                    widget.state(['!user1'])
            except tk.TclError:
                pass

        root.after(140, end_flash)

    def release(event):
        widget = event.widget
        if widget.winfo_toplevel() != root or widget.winfo_class() != 'TButton':
            return
        root.after_idle(clear_focus)

    def combo_selected(event):
        widget = event.widget
        if (widget.winfo_toplevel() is not root or widget.winfo_class() != 'TCombobox'
                or not widget.instate(('readonly',))):
            return

        def unselect():
            try:
                if widget.winfo_exists():
                    widget.selection_clear()
                    clear_focus()
            except tk.TclError:
                pass
        root.after_idle(unselect)

    root.bind_all('<ButtonPress-1>', press, add='+')
    root.bind_all('<ButtonRelease-1>', release, add='+')
    root.bind_all('<<ComboboxSelected>>', combo_selected, add='+')


def icon(root, name, active=False, *, color=None):
    """Use configurable burgundy for idle icons and original orange for selection.

    Active tabs/navigation reuse the packaged orange artwork, while the dark
    'ink' artwork on orange-filled buttons remains intact. Cache all variants
    for the lifetime of each Tk root; no recoloring during redraws.
    """
    cache = getattr(root, '_pytracker_icons', None)
    if cache is None:
        cache = {}
        root._pytracker_icons = cache
    if active == 'ink' or active is True:
        suffix = 'ink' if active == 'ink' else 'orange'
        key = (name, suffix)
        if key not in cache:
            cache[key] = tk.PhotoImage(master=root, file=str(_ASSETS / f'{name}-{suffix}.png'))
        return cache[key]
    color = (color or ICON_COLOR).upper()
    key = (name, False, color)
    if key not in cache:
        cache[key] = _tinted_icon(root, name, color)
    return cache[key]


def set_icon(root, widget, name, active=False, *, color=None):
    widget.configure(image=icon(root, name, active, color=color), compound='left')


def brand_logo(root):
    """Cache the dedicated project logo once per Tk root."""
    cache = getattr(root, '_pytracker_icons', None)
    if cache is None:
        cache = {}
        root._pytracker_icons = cache
    key = ('brand-logo', None)
    if key not in cache:
        cache[key] = tk.PhotoImage(master=root, file=str(_ASSETS / 'brand-logo.png'))
    return cache[key]


def style_listbox(widget):
    c = COLORS
    widget.configure(background=c['field'], foreground=c['text'],
                     selectbackground=c['selection'], selectforeground=c['accent_text'],
                     highlightbackground=c['border'], highlightcolor=c['accent'],
                     highlightthickness=1, relief='flat', borderwidth=0,
                     activestyle='none', selectborderwidth=0)


def style_text(widget):
    c = COLORS
    widget.configure(background=c['field'], foreground=c['text'],
                     insertbackground=c['accent'], selectbackground=c['selection'],
                     selectforeground=c['accent_text'], highlightbackground=c['border'],
                     highlightcolor=c['accent'], highlightthickness=1,
                     relief='flat', borderwidth=1, padx=8, pady=8)
