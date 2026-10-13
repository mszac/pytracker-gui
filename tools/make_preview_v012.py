"""Capture real v0.1.2 info bubble under Xvfb, using synthetic demo fixtures.

Not a runtime/hardware validation. Requires Pillow only for this developer-only screenshot.
"""
import shutil
import tempfile
import tkinter as tk
from pathlib import Path
from PIL import ImageGrab
from pytracker_gui.app import PytrackerGUI
from pytracker_gui.storage import save_settings
from pytracker_gui.help_widgets import InfoButton

ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    home=Path(tmp)
    upstream=home/'tobii-pytracker'
    demo=upstream/'tobii-pytracker-demo'
    (upstream/'src/tobii_pytracker').mkdir(parents=True)
    (upstream/'configs').mkdir()
    (upstream/'configs/mouse_eyetracker_config.yaml').write_text('mouse: true\n')
    (upstream/'configs/eyetracker_config.yaml').write_text('tobii: true\n')
    (upstream/'pyproject.toml').write_text('[build-system]\n')
    shutil.copytree(ROOT/'tests/fixtures/examples',demo/'examples')
    (demo/'tools').mkdir()
    (demo/'tools/run-demo.sh').write_text('#!/bin/bash\n')
    save_settings(home,{'upstream_root':str(upstream),'demo_root':str(demo)})
    tkroot=tk.Tk()
    tkroot.geometry('1190x830+20+20')
    gui=PytrackerGUI(tkroot,home=home)
    tkroot.update()
    gui.tabs.select(gui.pages['Monitor'])
    tkroot.update()
    def locate(widget,key):
        for child in widget.winfo_children():
            if isinstance(child,InfoButton) and child.help_key==key:
                return child
            found=locate(child,key)
            if found:return found
        return None
    bubble=locate(gui.pages['Monitor'],'display.monitor.width')
    assert bubble
    bubble.invoke()
    tkroot.update()
    im=ImageGrab.grab(bbox=(0,0,1280,900))
    im.save(ROOT/'docs/images/v012-linux-xvfb-parameter-help.png')
    gui.info_popover.dismiss()
    tkroot.destroy()
