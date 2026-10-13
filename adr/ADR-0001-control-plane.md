# ADR-0001 — GUI jako niezależny control plane
Status: PROPOSED (2026-10-10).

**Problem:** PsychoPy/ioHub/Tobii to ciężki i środowiskowo wrażliwy runtime; import w GUI ryzykowałby konflikt zależności, przywieszenia i duży footprint.

**Alternatywy:** (a) GUI zintegrowane z engine; (b) desktop launcher z osobnym child process; (c) web/electron serwer.

**Propozycja:** (b), izolowany runtime interpreter i state machine. Brak kopiowania trial loop i sensor logic. 

**Koszt:** adaptery procesu/cwd, synchronizacja statusu. **Zysk:** multiplatform, testowalność i lekkość.

**Walidacja:** cold start, idle memory, responsive running, identity of experiment output.
