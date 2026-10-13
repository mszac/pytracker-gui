# ADR-0036 — Fixed-size image buttons in the Home dashboard

**Date:** 2026-10-12. **Decision:** Accept. **Parent:** v0.2.17.

The user requested the four approved pictures instead of scalable solid-color dashboard tiles. The dashboard alone now uses pre-rendered 546×365 RGB PNG assets as clickable ttk button surfaces. The previous navigation contract is preserved; images and widgets retain a fixed pixel size regardless of window geometry. A small native Canvas viewport shows scrollbars only when a user shrinks the window below the required 2×2 area, avoiding inaccessible tiles. Runtime contains no Pillow/image processing, threads or polling.

Alternatives considered: stretching images with grid weights was rejected for violating fixed size; runtime Pillow resizing was rejected for footprint and processing overhead; permanently visible scrollbars were rejected as unnecessary at default geometry.

Known boundaries: fixed-size imagery is intentionally not DPI-responsive; captions are baked into the supplied English image assets, while localized text remains in button metadata. The existing GUI geometry changes with screen size; the chosen size corresponds to the actual measured initial Home tile on the current test display.
