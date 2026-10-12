# pytracker-gui v0.2.0 — charcoal and orange visual theme

## Scope
Presentation-only update of the existing v0.1.9 GUI, with no feature changes.
The navigation, Experiment / Logs / Diagnostics / Statistics screens, all six
experiment tabs, visible fields, YAML editor, help popovers, logs popup,
Start/Stop controls and project paths remain available as before.

## Implementation
- `pytracker_gui/theme.py` applies one static `ttk` palette using the built-in
  `clam` theme. Charcoal surfaces, near-white text, muted grays and an orange
  accent for selected navigation, tabs, demo rows and primary actions.
- The classic Tk widgets (`Listbox`, `ScrolledText` for instructions, YAML,
  reports and Experiment log, and `InfoPopover`) get matching dark colors.
  Small blue circular `i` icons still designate contextual help.
- Packaged compact PNG icons decorate the main navigation, tab headers and key
  actions. Each icon is loaded at most once per Tk root. No extra runtime
  graphics dependency is required. PNG files live in `pytracker_gui/assets/`.
- Initial window dimensions are computed once based on the available display,
  capped at 1300 × 960; existing minimum size and resize support remain.
- Additional modules are still constructed lazily. No animation loops,
  timers, new threads, subprocesses or background data scans were added.
- The native Windows title bar remains OS-controlled. This is a native Tk UI,
  not a pixel-exact replica of the concept rendering.

## Frozen behavior
Experiment configuration, profile persistence, yaml parsing, runtime child
launch/stop, logs, gaze, voice/raw settings, `projects/.../experiments/` storage,
upstream/demo source and measurement output are unchanged. Polish remains the
default language; English labels and help remain available. No theme selector yet.

## Validation and external gates
Linux/Python 3.13/Xvfb: 92/92 tests PASS (87 inherited + 5 presentation checks).
Verified cached icon use, static palette, laziness, lossless navigation during
unsaved YAML edits and language switching. Actual Tk screenshot:
`docs/images/v020-dark-orange-tk-preview.png`.
Windows 10/11, display scaling/DPI, and real PsychoPy/Tobii remain untested
here. Native ttk does not guarantee exact rounded shapes from the static mockup.
