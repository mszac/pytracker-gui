# ADR-0022 — Clickable brand and lazy module tile dashboard

Status: Accepted · 2026-10-11

## Context
A more prominent historic brand and a tile-style entry point are desired without
regressing the stable Experiment editor or adding rendering/analysis overhead.

## Decision
Keep the existing four top navigation actions. Add an explicit `home` destination
accessed by the brand name/mark. Construct a single native `DashboardScreen` only on
first access; its four buttons call `AppShell.select_screen`, exactly like top nav.
Keep `PytrackerGUI` persistent; it alone manages configuration and experiment process.
Lighter orange and higher-resolution build-time PNGs remain static ttk/Tk visuals.
Selected notebook-tab horizontal padding is mapped to half its old value; font sizes
outside the brand/dashboard are unchanged. No other behavior or state schema changes.

## Consequences
There is one more optional Tk frame and four buttons after the first brand click,
with no background work. Additional modules may be implemented independently later.
Windows DPI rendering requires hardware inspection. No compatibility migration.
