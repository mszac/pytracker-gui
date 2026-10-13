# ADR-0006 — Completeness gate, append-only engineering logs
Status: PROPOSED (2026-10-10).

**Problem:** exit code 0 może współistnieć z logowanym błędem albo brakującym plikiem; historyczne problemy wracają bez zapisanego dowodu.

**Propozycja:** run COMPLETE jedynie na PASS collection checks; oddzielny gaze quality status. W każdej iteracji append-only: CHANGELOG, DECISION_JOURNAL, WORK_SESSION_LOG, VALIDATION_LOG, PROJECT_CONTINUITY_LOG, KNOWN_ISSUES.

**Wpis decyzji:** obserwacja, hipoteza/alternatywy, wybór, motywacja/trade-off, dowód/test, niepewność, następny krok — zwięzła techniczna dokumentacja, nie ukryty prywatny tok myśli.
