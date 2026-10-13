# ADR-0041 — Independent small-icon tint parameter (v0.2.24)

**Decision:** Keep the global orange palette as frozen. Introduce `theme.ICON_COLOR = '#C77D8F'` as the only configurable small-icon tint parameter. Do not add a visible GUI Settings control or change the project logo, fixed dashboard artwork, or the dark ink icons required on orange-filled buttons.

**Implementation rationale:** Preserve the existing antialiased geometry with a deterministic precomputed alpha-only mask (~16 KiB for 19 icons). On-demand stdlib zlib/PNG encoding and per-Tk-root caching avoid additional runtime dependencies, timers or ongoing computation. The color value is a real hexadecimal input to image construction, rather than a label selecting fixed assets, making future preference binding straightforward.

**Guardrails:** No changes to experiment/process/storage/YAML/log/Manual code. Navigation selection identities remain distinct; selected text and backgrounds remain orange. No automatic persistence or live widget rebind is introduced now. Verify orange accent invariants, ink contrast, user-configurable hex, cache, pixel dimensions, GUI navigation and byte-frozen unrelated assets.
