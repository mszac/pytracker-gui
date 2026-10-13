# ADR-0015 — Equal PL/EN documentation coverage without expanding M1 runtime

**Date:** 2026-10-11
**Status:** Accepted for v0.1.4
**Parent:** v0.1.3-bilingual-ui

## Context

The Polish help catalog already contained 87 short and extended descriptions; the English overlay had only 87 titles and short popovers. Historical install guides and the GUI manual-location note therefore implied incomplete English documentation. Some wording could be mistaken for executable control of original PsychoPy demos even though pytracker-gui is still a configuration editor.

## Decision

1. Retain stable schema keys and the Polish catalog as the registry for availability, source URL and category. Add long English descriptions to the existing English overlay. Do not translate YAML/CLI identifiers or enum literals.
2. Generate both full Markdown manuals from these two JSON resources; preserve `render()` as the Polish compatibility API and extend the same generator and `--check` to English.
3. Publish equivalent current PL/EN installation and user guides and document language pairs through separate indexes. Preserve historical logs and ADRs instead of retroactively translating or rewriting their decisions.
4. Clarify every `gui`, `yaml-only`, `iohub-only`, `reference`, `future` status. Distinguish static editing/profiles/dry-run from experimental execution and distinguish no-gaze from mouse answers, AOE from AOI and generic upstream MouseGaze from specialized adapters.
5. Only revise the GUI's *informational label* to name both manual files, without adding a link or window. The help bubbles continue to show exactly the short localized text.

## Consequences and validation

Documentation becomes approximately symmetric for 87 current parameters; the GUI only gains more accurate visible file names. No new external dependencies, backend bridge, ioHub editor, experiment start/stop or profile migrations. Validate deterministic PL+EN generation, bilingual key/status/source alignment, current guides and all inherited regressions. Full Windows/Python 3.10/PsychoPy/ioHub and Tobii verification remains a separate requirement. Original upstream and demo repositories are read-only sources.
