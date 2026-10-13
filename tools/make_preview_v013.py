"""Capture both UI languages from the same GUI and fixture, without Tobii/PsychoPy.

Developer-only image creation; Pillow is not a runtime dependency.
"""
import shutil
import tempfile
import tkinter as tk
from pathlib import Path
from PIL import ImageGrab
from pytracker_gui.app import PytrackerGUI
from pytracker_gui.storage import save_settings
from pytracker_gui.help_widgets import InfoButton

ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    home = Path(tmp)
    upstream = home/'tobii-pytracker'
    demo = upstream/'tobii-pytracker-demo'
    (upstream/'src/tobii_pytracker').mkdir(parents=True)
    (upstream/'configs').mkdir()
    (upstream/'configs/mouse_eyetracker_config.yaml').write_text('mouse: true\n')
    (upstream/'configs/eyetracker_config.yaml').write_text('tobii: true\n')
    (upstream/'pyproject.toml').write_text('[build-system]\n')
    shutil.copytree(ROOT/'tests/fixtures/examples', demo/'examples')
    (demo/'tools').mkdir()
    (demo/'tools/run-demo.sh').write_text('#!/bin/bash\n')
    save_settings(home, {'upstream_root':str(upstream), 'demo_root':str(demo)})
    root = tk.Tk()
    root.geometry('1190x830+30+30')
    gui = PytrackerGUI(root, home=home)
    gui.tabs.select(gui.pages['Monitor'])
    root.update()
    def icon_for(widget, key):
        for child in widget.winfo_children():
            if isinstance(child, InfoButton) and child.help_key == key:
                return child
            result = icon_for(child, key)
            if result:return result
        return None
    button = icon_for(gui.pages['Monitor'], 'display.monitor.width')
    for language, filename in (('pl', 'v013-polish-help.png'), ('en', 'v013-english-help.png')):
        if language == 'en':
            gui.language_name.set('English')
            gui._on_language_changed()
        root.update()
        button = icon_for(gui.pages['Monitor'], 'display.monitor.width')
        button.invoke()
        root.update()
        ImageGrab.grab(bbox=(0,0,1320,940)).save(ROOT/'docs/images'/filename)
        gui.info_popover.dismiss()
    root.destroy()
