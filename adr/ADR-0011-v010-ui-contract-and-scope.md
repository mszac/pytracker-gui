# ADR-0011 — pierwszy działający GUI: edytor kontrolny, nie fałszywy launcher

**Status:** implemented for v0.1.0, 2026-10-10.
**Context:** user requested a concrete interface implementation grounded in approved M1, including 7 variants and YAML editing before implementation of runtime bridge. Original phase A alone had no YAML editing, while phase B called for more complete settings and ioHub control.
**Alternatives:** (a) static wireframe only; (b) call existing wrappers directly from GUI despite hardcoded flags; (c) targeted functional editor with backend intentionally disabled.
**Decision:** (c) implement Tk shell + robust subset of phase B: source config round-trip editor, structured forms, profiles, static preflight; do not expose a working Run button yet.
**Why:** provides immediate usability for configuration/profiles without silently ignoring gaze/voice/raw settings. Keeps heavy dependencies out of GUI and upstream sources immutable.
**Constraints:** keep all 7 variants, time-series 2 blocks, persistent per-demo profile; no claimed experimental/hardware proof; per-file checksums/rollback; preserve unknown YAML/comments but note whitespace need not be byte-identical.
**Unresolved:** full ioHub YAML editing, protocol-native launcher, adapter bridge, Windows hardware tests, exact upstream SHA, end-to-end config validation.
