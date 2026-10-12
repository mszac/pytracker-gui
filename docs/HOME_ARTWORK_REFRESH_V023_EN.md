# Home dashboard artwork refresh — v0.2.23

This release replaces exactly four pre-rendered Home image assets with the approved saturated blue, cyan and orange variants: Experiments, Logs, Statistics and Manual. Source images are the four corresponding user-supplied `*2.png` files.

Each image was center-cover cropped (aspect-ratio preserved), Lanczos downsampled to exactly **546 × 365 pixels**, converted to RGB and saved as an optimized PNG. Resulting on-disk sizes are less than 350 KiB each. There is **no Pillow dependency during GUI execution**, no runtime resizing, new widget, animation or network request. The images retain their old asset filenames and their existing four screen routes.

The sole runtime differences against v0.2.22 are the four image bytes and the v0.2.23 release identifier. `pytracker_gui/screens.py`, `shell.py`, GUI Settings, PsychoPy integration, project storage, logs and all other runtime modules are unchanged.

Validation gate: identical asset dimensions, bounded size, original screen routing, imported GUI, source freeze, manifests and clean unpack of both ZIP variants. Physical Windows/HiDPI verification remains external.
