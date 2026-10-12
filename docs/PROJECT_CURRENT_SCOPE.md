# Aktualny scope i priorytety — read this first

Current accepted milestone: `M1 EXISTING DEMOS CONTROL` (docs/M1_SCOPE_AND_ACCEPTANCE.md). All v0.0.0 docs remain as the preserved historical planning baseline and may contain now-deferred work (wizard/new experiment). Superseding docs are dated 2026-10-10 and have priority when inconsistent with older documents. Read `docs/DEMO_LAUNCH_MATRIX.md` and `docs/CONFIG_CONTROL_MATRIX.md` before implementation. No code exists as of v0.0.1.

Suggested versions: v0.1.0 environment+catalog; v0.2.0 config/control; v0.3.0 native launch 7 variants; v0.4.0 all three gaze modes/flags; v0.5.0 milestone acceptance. Version numbers are plans, not releases. Future novel experiment design will be planned only after M1 acceptance.

## v0.1.0 UI checkpoint (2026-10-10)
Current installed functionality: seven existing variants + eight native config blocks, editable copy main YAML, gaze selector and path, validation/profiles. This is not full M1. Creating new experiments remains deferred. Run/stop is intentionally not implemented before tested child bridge. See `docs/UI_PROTOTYPE_V010.md`.

## v0.1.1 canonical layout correction (2026-10-11)
Nested checkouts now required: original tobii-pytracker checkout containing tobii-pytracker-demo and pytracker-gui children. See `NESTED_REPOSITORY_CONTRACT_V011.md` and `INSTALL_AND_USE_V011_GIT_BASH_WINDOWS.md`. Launch remains disabled; M1 not complete.

## v0.1.4 documentation-only update (2026-10-11)
Both language editions now cover the same 87 source parameters, their availability/status and current M1 editor behavior. Refer to `docs/DOCUMENTATION_INDEX_PL.md` and `docs/DOCUMENTATION_INDEX_EN.md`. Demo launch/stop, physical hardware and ioHub internal editing remain pending; documentation parity does not complete M1 or replace platform validation.

## v0.1.8 modular navigation (2026-10-11)
The existing demo configuration and launch screen is now hosted by a lightweight top-level AppShell. New Logs / Diagnostics / Statistics screens are independent lazy placeholders; browsing/analysis are deliberately not implemented. Runtime, storage and six experiment tabs remain unchanged. See `NAVIGATION_SHELL_V018_PL.md` and `NAVIGATION_SHELL_V018_EN.md`.
