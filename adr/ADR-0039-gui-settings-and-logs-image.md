# ADR-0039 — scoped GUI Settings and replacement Logs home artwork

Date: 2026-10-12

Decision: keep v0.2.20/v0.2.21 non-settings runtime frozen. Replace only the Home Logs static PNG with the approved user asset. Add a lazily instantiated GUI Settings page after Manual; reuse the existing color palette, local compact cards, and local GUI settings.json. Let the page persist a validated window-size preset only, with effect at next startup. Display, but do not create competing writers for, repository and interpreter paths; Experiment → Environment remains authoritative. The panel performs no PsychoPy, YAML or results I/O, no timers and no background work.

Reason: a useful first settings page without new configuration ownership or runtime pressure on experiments.

Limitations: Windows/HiDPI physical visual verification is pending; output directories and scientific results remain wholly owned by experiment code.
