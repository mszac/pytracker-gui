# ADR-0042 — Restore original selected orange icons (v0.2.25)

**Decision:** Change only the small-icon idle tint to `#A9526B` and use the existing original `*-orange.png` artwork when `active is True`. Keep `active='ink'` on orange-filled buttons and `ICON_COLOR` as the sole future-customizable idle tint parameter.

**Rationale:** v0.2.24 tinted active and idle icons identically even though selected labels remained orange. Reusing packaged orange art restores the prior state contract with no new image dependency, background work, or runtime resource generation.

**Scope:** Production change only to `pytracker_gui/theme.py` and version identity. Keep other source and asset bytes unchanged. Historical v0.2.24 assertions for a now-superseded default are updated as a regression gate; add focused state tests and cumulative documentation.
