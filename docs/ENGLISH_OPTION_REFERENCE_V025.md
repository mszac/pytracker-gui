# v0.2.5 — Starter-project terminology and English option reference

## Scope

The user-facing GUI now calls the supplied seven example configurations **starter projects** rather than treating demonstrations as the application's only purpose. The selected **starter project** determines the initial example configuration; the user-owned **project** retains its separate identity and files under `projects/<name>/`. Internal catalog IDs, underlying repository names, source file paths, run manifests, and the actual runtime remain unchanged.

## Documentation policy

English is the editorial baseline for future parameter descriptions. The previously released **Polish parameter catalogue and `PARAMETER_MANUAL_PL.md` remain unchanged in this release**. Translating new option-level notes into Polish is explicitly deferred and should be handled as a separate reviewed iteration.

The English overlay `pytracker_gui/parameter_help_en.json` contains **28 `options` entries (70 documented option values)**. Only parameters that expose a constrained list or a documented switch/mode have an **Available options** section. Other parameters remain free-entry numeric, path, name, color, or structured YAML fields and have no invented option list. Choices are also visible in the English in-app Manual screen, are searchable by value and description, and are never treated as interactive controls that modify configuration.

Option status is important: `gui` means the current GUI exposes the field, `reference` means the option is documented in upstream but may not have a dedicated control, `iohub-only` means the YAML is not edited by the GUI, and `future` remains unsupported here. MouseGaze 50/100 Hz are documented emulator values; Tobii sampling rates are hardware-specific. `CIRCLE_TARGET`, `rgb` and `pix` describe the known configuration, not proof that every other driver alternative works.

## Sources and verification

- Original upstream `configs/config.yaml` — image/text/time-series region model values
- Original upstream `configs/mouse_eyetracker_config.yaml` — mouse controls, supported sampling rates, target/calibration settings
- Original upstream `configs/eyetracker_config.yaml` — binocular Tobii settings and calibration configuration
- Original upstream `src/tobii_pytracker/main.py` — launch flags, session mode, logging levels
- The current GUI's `fields.py`, `catalog.py` and runtime bridge — exactly which options the UI exposes and which projects/blocks are selectable

The documentation describes known upstream configuration contracts; it does not assert that each optional setting has been exercised successfully with physical Tobii hardware.
