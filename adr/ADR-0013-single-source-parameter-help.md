# ADR-0013 — Single-source parameter help and click-only info icons

Date: 2026-10-11 | Status: Accepted for v0.1.2.

**Problem.** M1 exposes numerous YAML fields and runtime preferences, but labels alone are insufficient for nontechnical operators. Duplicating short help strings in widget code and long reference descriptions in Markdown would cause drift. The manual must also distinguish editable fields from source-only ioHub/CLI parameters.

**Decision.** Keep a UTF-8 `pytracker_gui/parameter_help.json` catalog with unique stable parameter keys, a one-sentence Polish `short` description, a multi-sentence Polish `long` description, provenance URL and a status indicating editability. Tkinter reads only `short` for its small blue circular `i` icons. A deterministic renderer creates `docs/PARAMETER_MANUAL_PL.md` from the same catalog; tests compare them byte-for-byte. Source-only ioHub fields appear in the manual but are not given phantom edit controls. No GUI link to the manual in this release.

**UI policy.** Use stock Tk Canvas circles and `Toplevel` popovers rather than icon assets, browsers, external libraries or implicit hover actions. Click, Enter or Space opens or toggles a compact help bubble; the bubble has a close control and Escape handling. Popovers are destroyed before re-rendering forms. The help system cannot modify YAML, profiles or runtime settings.

**Alternatives rejected.** Hover-only tooltip (hard to discover, fragile with touch/accessibility), duplicated hard-coded help strings, embedding the entire long manual into each bubble, and adding a web/manual link before the manual navigation specification is accepted.

**Risks and gates.** Windows high-DPI placement and keyboard navigation require a real-machine test. Long documentation should be reviewed against an exact pinned Git SHA before becoming normative advice. The GUI still does not launch experiments or edit ioHub internals; these are separate scope items.
