"""Developer-only screenshot of Launch tab; no runtime, hardware or network."""
import tempfile, shutil, tkinter as tk
from pathlib import Path
from PIL import ImageGrab
from pytracker_gui.app import PytrackerGUI
from pytracker_gui.storage import save_settings
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    home=Path(tmp)
    up=home/'tobii-pytracker'; demo=up/'tobii-pytracker-demo'
    (up/'src/tobii_pytracker').mkdir(parents=True)
    (up/'configs').mkdir()
    (up/'pyproject.toml').write_text('[build-system]\n',encoding='utf8')
    (up/'configs/mouse_eyetracker_config.yaml').write_text('mouse: true\n')
    (up/'configs/eyetracker_config.yaml').write_text('tobii: true\n')
    shutil.copytree(ROOT/'tests/fixtures/examples',demo/'examples')
    (demo/'tools').mkdir();(demo/'tools/run-demo.sh').write_text('#!/bin/bash\n')
    save_settings(home,{'upstream_root':str(up),'demo_root':str(demo),'language':'pl'})
    root=tk.Tk();root.geometry('1190x830+20+20')
    gui=PytrackerGUI(root,home=home)
    gui.tabs.select(gui.pages['Uruchomienie']);root.update()
    ImageGrab.grab(bbox=(0,0,1300,900)).save(ROOT/'docs/images/v015-launch-tab.png')
    root.destroy()
