# ADR-0004 — Jawny CWD i launch recipe zamiast zależności od powłoki
Status: PROPOSED (2026-10-10).

**Problem:** YAML paths i output zależą od CWD, wrappery demonstracji są Bash i różnią się opcjami/walidacją.

**Propozycja:** immutable `RunSpec`, explicit cwd, Python `Popen` argv (bez shell), audytowany registry launch/validate per demo. Wrappery shell pozostają referencyjnym oracle w testach parity. Windows nie wymaga Git Bash do docelowego GUI.

**Walidacja:** każda demo/EN/PL/machine+PV ma identyczne collection output; Windows path spaces, log capture.
