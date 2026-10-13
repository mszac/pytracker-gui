# ADR-0038 — Environment icon size adjustment only

Date: 2026-10-12

Decision: enlarge the Save paths icon's visual mark within its existing 40×40 canvas, and use the existing full-size 40×40 folder icon on Detect layout. Keep Check Python at 20×20 and Load repository untouched. Reuse the root-owned Tk icon cache and pre-rendered resources; no runtime image processing. All button actions and styles remain unchanged.

Scope: minor UI-only direct child of exact v0.2.19 Full. Confirm on physical Windows at current DPI before considering further UI adjustments.
