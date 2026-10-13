# ADR-0005 — Osobna metadana projektu i wygenerowany YAML upstream
Status: PROPOSED (2026-10-10).

**Problem:** nowe pojęcia GUI (participant code, projekt, stan walidacji, run ID) nie istnieją automatycznie w `CustomConfig`/data.csv.

**Propozycja:** project.json w własnym workspace, generated main/tracker YAML tylko z potwierdzonych upstream fields, immutable run snapshot, nie mutować demo/engine ani nie dopisywać nieobsługiwanych pól YAML.

**Walidacja:** trzy modality real runs, schema round trip, output provenance.
