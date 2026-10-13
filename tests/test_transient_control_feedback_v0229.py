"""Regression: transient button activation and non-editable combo focus."""
import tkinter as tk
import unittest
from tkinter import ttk
from pytracker_gui.theme import apply_theme


class FeedbackTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        apply_theme(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_button_flash_is_bounded(self):
        for style in ('TButton', 'Accent.TButton', 'Brand.TButton'):
            button = ttk.Button(self.root, text='Action', style=style)
            button.pack()
            self.root.update()
            button.event_generate('<ButtonPress-1>')
            self.root.update()
            self.assertTrue(button.instate(('user1',)))
            self.root.after(190, self.root.quit)
            self.root.mainloop()
            self.assertFalse(button.instate(('user1',)))

    def test_flash_precedes_release_and_command_is_not_delayed(self):
        observed = []
        button = ttk.Button(self.root, text='Action',
                            command=lambda: observed.append(button.instate(('user1',))))
        button.pack()
        self.root.update()
        button.event_generate('<ButtonPress-1>', x=3, y=3)
        self.assertTrue(button.instate(('user1',)))
        self.assertEqual(observed, [])
        button.event_generate('<ButtonRelease-1>', x=3, y=3)
        self.assertEqual(observed, [True])

    def test_readonly_combobox_deselects_text_without_losing_value(self):
        combo = ttk.Combobox(self.root, state='readonly', values=['1300 x 960'])
        combo.pack()
        combo.set('1300 x 960')
        combo.selection_range(0, 'end')
        combo.event_generate('<<ComboboxSelected>>')
        self.root.update()
        self.assertEqual(combo.get(), '1300 x 960')
        self.assertFalse(combo.selection_present())

    def test_selected_navigation_is_excluded(self):
        radio = ttk.Radiobutton(self.root, text='Selected', style='Toolbutton')
        radio.pack()
        radio.event_generate('<ButtonRelease-1>')
        self.root.update()
        self.assertFalse(radio.instate(('user1',)))

    def test_dashboard_images_do_not_flash(self):
        button = ttk.Button(self.root, style='DashboardImage.TButton')
        button.pack()
        button.event_generate('<ButtonPress-1>')
        self.root.update()
        self.assertFalse(button.instate(('user1',)))


if __name__ == '__main__':
    unittest.main()
