# v0.2.14 — Logs stage 2: bounded console journal and accessible selection

## Scope

Built directly on exact v0.2.13. The **Console Log** tab is now operational for a selected project/run; existing experiment journaling and configuration snapshots are unchanged. Typography is increased one step **only on Logs** (selectors, labels, cards, buttons and console). A screen-local light orange selection `#FFC187` with dark ink `#131820` replaces the previous low-contrast highlight. The global v0.2.6 palette and other screens are byte-frozen.

## Contract

- Selecting a run retains the Settings report. Journal I/O starts only after a user selects Console Log. Settings rendering, YAML detail expansion and selection are not journal readers.
- Only the precisely matching `experiment_<start_YYYYMMDD_HHMMSS>_<5-char-ID>.log[.part]` for the run is eligible. An incomplete `.part` takes precedence when both exist. Missing journals are expected and handled without exceptions.
- Controls: **First**, **Previous**, **Next**, **Latest**, **Refresh log**, **Copy page**; vertical and horizontal scrollbars. A growing `.part` is refreshed manually; no watcher, polling or automatic refresh.
- Per-page read is bounded to **64 KiB and 2,000 text lines**, with explicit seek and UTF-8 replacement for malformed input. No whole-file load, measurement CSV read, new runtime worker, Sphinx/HTML engine or database.
- COMPLETE/INCOMPLETE describe journal integrity only, not whether an experiment succeeded. `.part` repair is intentionally deferred. Console Log never writes to project files or changes log lifecycle.

## Performance / caveats

Very long lines may need horizontal scrolling; a UTF-8 multibyte character split by a 64-KiB hard boundary can show a replacement glyph on the preview page only. During acquisition the low-priority writer might still hold the most recent lines in its existing 256-KiB pending buffer, so **Refresh log** shows only bytes actually written to disk. All disk I/O is triggered by selecting Console Log or one of its controls and is capped by a small read; it does not enter the PsychoPy subprocess or incremental writer.

## Windows acceptance gate

Inspect selection contrast/font sizes at standard/HiDPI, traverse a large log, check `Latest`, horizontal scrolling, clipboard of the visible portion, manually refresh an active `.part`, and verify no change to live Auto-show Logs and settings report. Physical Windows/PsychoPy/Tobii acceptance is still untested under the Linux/Xvfb host.
