"""Lightweight Tk-only circular info icons and click-activated popovers."""
import tkinter as tk
from tkinter import ttk
from .theme import COLORS

BLUE = '#6caed8'  # subdued blue keeps the established info affordance


class InfoButton(tk.Canvas):
    """Keyboard-operable circular blue 'i' control, independent of theme."""
    def __init__(self, parent, *, help_key, callback):
        super().__init__(parent, width=19, height=19, bd=0, highlightthickness=0,
                         takefocus=1, background=parent.cget('background') if 'background' in parent.keys() else COLORS['surface'],
                         cursor='hand2')
        self.help_key = help_key
        self.callback = callback
        self.create_oval(2, 2, 17, 17, fill=BLUE, outline=BLUE)
        self.create_text(9.5, 9.5, text='i', fill='white', font=('TkDefaultFont', 10, 'bold'))
        self.bind('<Button-1>', self._activate)
        self.bind('<Return>', self._activate)
        self.bind('<space>', self._activate)
        self.bind('<FocusIn>', lambda _e: self.configure(highlightthickness=1, highlightbackground=BLUE))
        self.bind('<FocusOut>', lambda _e: self.configure(highlightthickness=0))

    def _activate(self, _event=None):
        self.focus_set()
        self.callback(self, self.help_key)
        return 'break'

    def invoke(self):
        """Testable click action, equivalent to mouse or keyboard activation."""
        return self._activate()


class InfoPopover:
    """At most one non-modal speech bubble; close by X, Escape or another icon."""
    def __init__(self, root, help_lookup, on_manual=None):
        self.root = root
        self.help_lookup = help_lookup
        self.on_manual = on_manual
        self.popup = None
        self.active = None

    def dismiss(self):
        popup = self.popup
        self.popup = None
        self.active = None
        if popup is not None:
            try:
                if popup.winfo_exists(): popup.destroy()
            except tk.TclError:
                pass

    def _open_manual(self, key):
        self.dismiss()
        if self.on_manual is not None:
            self.on_manual(key)

    def toggle(self, anchor, help_key):
        if self.popup is not None and self.active == help_key and self.popup.winfo_exists():
            self.dismiss()
            return
        self.dismiss()
        help_record = self.help_lookup(help_key)
        if not help_record.get('short'):
            raise ValueError('Missing short parameter help: ' + help_key)
        popup = tk.Toplevel(self.root)
        popup.withdraw()
        popup.overrideredirect(True)
        popup.configure(background=COLORS['border'])
        shell = tk.Frame(popup, background=COLORS['surface_alt'], borderwidth=0)
        shell.pack(padx=1, pady=1, fill='both', expand=True)
        head = tk.Frame(shell, background=COLORS['surface_alt'])
        head.pack(fill='x', padx=10, pady=(8, 2))
        tk.Label(head, text=help_record['title'], font=('TkDefaultFont', 10, 'bold'),
                 foreground=COLORS['text'], background=COLORS['surface_alt']).pack(side='left', anchor='w')
        tk.Button(head, text='×', relief='flat', borderwidth=0, font=('TkDefaultFont', 13),
                  background=COLORS['surface_alt'], foreground=COLORS['muted'], cursor='hand2',
                  command=self.dismiss).pack(side='right')
        tk.Label(shell, text=help_record['short'], wraplength=285, justify='left',
                 background=COLORS['surface_alt'], foreground=COLORS['text'], padx=10, pady=6).pack(fill='x')
        if self.on_manual is not None:
            link = tk.Label(shell, text='man', font=('TkDefaultFont', 10, 'bold', 'underline'),
                            foreground=COLORS['accent'], background=COLORS['surface_alt'],
                            cursor='hand2', padx=10, pady=4)
            link.pack(anchor='e')
            link.bind('<Button-1>', lambda _event, key=help_key: self._open_manual(key))
            link.bind('<Return>', lambda _event, key=help_key: self._open_manual(key))
            link.bind('<space>', lambda _event, key=help_key: self._open_manual(key))
            link.configure(takefocus=1)
        popup.bind('<Escape>', lambda _e: self.dismiss())
        popup.update_idletasks()
        width = max(220, popup.winfo_reqwidth())
        height = popup.winfo_reqheight()
        x = anchor.winfo_rootx() + anchor.winfo_width() + 4
        y = anchor.winfo_rooty() - 5
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        if x + width > screen_width - 12:
            x = max(0, anchor.winfo_rootx() - width - 4)
        y = max(0, min(y, screen_height - height - 12))
        popup.geometry(f'{width}x{height}+{x}+{y}')
        popup.deiconify()
        popup.lift()
        self.popup = popup
        self.active = help_key
