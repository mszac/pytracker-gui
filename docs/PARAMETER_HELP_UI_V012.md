> **Historia / historical checkpoint:** Ten dokument opisuje wyłącznie zakres swojego wydania. Aktualne przewodniki i manuale PL/EN w `docs/DOCUMENTATION_INDEX_PL.md` / `docs/DOCUMENTATION_INDEX_EN.md` zastępują nieaktualne twierdzenia o braku angielskiego manuala.

# v0.1.2 — parameter documentation and info buttons

This is an implementation contract, not a user-facing GUI link to the manual.

## Source references

- Original runtime `sbobek/tobii-pytracker` README (general YAML schema and CLI): https://github.com/sbobek/tobii-pytracker
- Upstream general config: https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/config.yaml
- Upstream MouseGaze configuration: https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml
- Upstream Tobii configuration: https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/eyetracker_config.yaml
- Demonstration repository `mszac/tobii-pytracker-demo` v1.17.0: https://github.com/mszac/tobii-pytracker-demo ; original provided archive supplies the exact eight YAML baseline configurations.

No exact live Git SHA was resolved in the offline container: references to branch `main` are current-source evidence, not immutable code provenance. Windows operator should record both `git rev-parse HEAD` values for future schema checks.

## Implementation

- `pytracker_gui/parameter_help.json` contains 87 unique keys with `title`, `short`, `long`, `group`, `status`, `source`.
- `status=gui` fields can be edited/selected; `yaml-only` fields exist in upstream but are not separately displayed in form; `iohub-only` entries are reference descriptions and **not editable** inside the GUI; `reference` entries refer to upstream CLI flags that have not yet been connected; `future` denotes out-of-scope behavior.
- `tools/render_parameter_manual.py` converts the one authoritative catalog into `docs/PARAMETER_MANUAL_PL.md`. `--check` compares deterministic Markdown with expected output.
- Tkinter `InfoButton` is drawn as a true blue circle with a white letter `i`, accessible via click, Return or Space; the one-sentence popover shows only `short`, not `long` or a link.
- `InfoPopover` is nonmodal, supports toggle/X/Escape/outside-click dismissal and is destroyed on form refresh. No hover-based behavior, external icon files, network calls or hyperlink controls.
- View changes are help-only. The field and profile storage path, schema validation and original source protection have not been changed.

## Regression gates

1. Each `Field.path` in every form resolves to a documented key.
2. All leaf YAML paths of the eight supplied fixture configs have descriptions.
3. Every displayed GUI help key is validated against the catalog before the control is built.
4. Descriptions are nonempty, short help is single-sentence; the Markdown manual is synchronized exactly to JSON.
5. Tk tests assert `i` buttons are blue, popovers show the short string, toggling/selection works and tab changes dismiss stale bubbles.
6. All older layout, seven-demo, profile and YAML round-trip tests remain passing.

## Boundaries

Neither this release nor the documentation renderer launches a demo, edits internal ioHub files, or introduces a manual hyperlink. The manual is written in Polish to match the current form language, while the additional standalone Windows setup README is in English. Physical Windows/Tobii behavior and high-DPI coordinates are unverified.
