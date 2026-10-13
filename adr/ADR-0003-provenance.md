# ADR-0003 — Pinned runtime provenance i brak nadpisywania upstream
Status: PROPOSED (2026-10-10).

**Problem:** publiczny branch i historyczne dokumenty mogą się różnić; ZIP demo nie zawiera pełnego upstream source.

**Propozycja:** preflight wymaga oryginalnego upstream i zapisuje SHA/wersje; wydania nie edytują upstream; copy-on-write config; run manifest + hashes. Nie certyfikować SHA bez wykonanej fizycznej bramki.

**Walidacja:** check środowiska, source clean, identyczny input/output przed/po działaniu GUI, run manifest.
