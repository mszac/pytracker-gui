"""Produce a screenshot of the real Tk interface under a graphical X session."""
import tempfile
import tkinter as tk
from pathlib import Path
from PIL import ImageGrab
from pytracker_gui.app import PytrackerGUI

with tempfile.TemporaryDirectory() as tmp:
    home=Path(tmp)
    root=tk.Tk()
    gui=PytrackerGUI(root,home=home)
    root.update()
    root.geometry('1190x830+20+20')
    root.update()
    im=ImageGrab.grab(bbox=(0,0,1235,890))
    im.save(Path(__file__).resolve().parents[1]/'docs/images/v011-linux-xvfb-preview.png')
    root.destroy()
