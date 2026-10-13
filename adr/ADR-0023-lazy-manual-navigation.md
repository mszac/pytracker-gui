# ADR-0023 — Lazy, read-only manual with contextual deep links

Date: 2026-10-11
Status: Accepted

## Context

The established Tk interface uses brief `i` tooltips and already contains two complete, aligned catalogs with 87 extended parameter descriptions. The user requested a fifth independent Manual screen plus a `man` link in each popover, with no changes to experiment runtime or project persistence.

## Decision

Implement Manual as a lazily created, retained `ttk.Frame` under the existing `AppShell`; use a small search-driven list/detail UI and existing cached catalogs. Contextual popovers navigate by stable parameter key, preserving the live Experiment frame and uncommitted YAML. Keep the GUI language and documentation language independent as before. Use a small PNG with a white circular backing behind the pre-existing brand mark, removing the old orange diamond; do not replace the application's brand action.

## Alternatives rejected

An external browser/manual server, a duplicate documentation database, eager construction at startup, polling or indexing project files, adding a separate manual window, and changing the experiment notebook.

## Consequences and checks

No additional runtime packages, threads, timers, background file readers or experiment I/O. The bundle includes a few small PNG assets. Validate key coverage and deep links with Tk/Xvfb tests, and preserve all previous runtime/project modules byte-for-byte.
