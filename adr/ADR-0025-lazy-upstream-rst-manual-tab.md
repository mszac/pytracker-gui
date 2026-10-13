# ADR-0025 — Separate local upstream RST documentation from parameter index

Date: 2026-10-11

## Decision

The existing Manual is the default **Index** tab. Add a **Documentation** tab that
reads only `docs/**/*.rst` from the currently selected original `tobii-pytracker`
checkout. It does not read `tobii-pytracker-demo`, copy documentation into the GUI,
fetch network content, render Sphinx, or modify a source file. The initial
Documentation tab visit lazily discovers filenames; choosing a file reads and shows
its unmodified UTF-8 source with lightweight heading emphasis. A changed upstream
path is rescanned only after opening that tab again. File size is bounded to 2 MiB.

Existing tooltip `man` links always target a parameter in Index, even when
Documentation is currently selected. English selectable option **values** use the
green success color, while the `Available options` heading retains its distinct
muted heading color. No field editing, process launch, persistence or project
storage logic changes.

## Motivation and tradeoffs

A read-only Tk text reader and file list use only stdlib/Tk and are cheap when
unused. Source RST remains faithful but advanced Sphinx directives, substitutions,
figures and inter-file links are displayed as source rather than rendered HTML.
Those features can be reviewed separately; no heavy documentation dependency was
added to the active GUI or its experiment process.
