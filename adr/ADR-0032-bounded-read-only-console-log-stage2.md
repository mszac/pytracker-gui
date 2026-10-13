# ADR-0032 — bounded, exact-run, read-only Console Log (v0.2.14)

**Context.** The first-stage Logs dashboard exposes projects/runs and immutable settings but leaves Console Log disabled. The user requires a useful low-cost viewer, slightly larger type and a more legible orange selection; the PsychoPy acquisition and existing 256-KiB background journal writer must remain untouched.

**Options.** Loading the whole log into `tk.Text` is easy but unbounded. Tail-following with periodic polling competes with the experiment disk. A background indexing task and log database increase complexity and ongoing I/O. Native paged reads triggered by user action are simpler.

**Decision.** Add a pure bounded reader with exact filename agreement on run timestamp and case-sensitive ID, a 64-KiB/2,000-line cap, on-demand first/previous/next/latest navigation and a manual Refresh for `.part`. A read-only `tk.Text` with scrollbars renders only the selected page. The existing six-card Settings UI and state remain; switching run defaults to Settings. Use local font sizes and local `#FFC187` selection (black text), never alter global theme. Preserve the `.log`/`.log.part` producer untouched.

**Security/robustness.** Reject symlink files and nonregular files; avoid unrestricted path traversal and ensure journal names exactly match the run identity. Distinguish completeness of the journal from successful PsychoPy execution. Bound read operations; cope with absent, changing or undecodable log content. Fail with a visible message, not a traceback in the GUI.

**Trade-offs.** On-demand reading may wait briefly for an already-contended disk, but not in the PsychoPy reader or log writer threads. No instant live follow. Very long unbroken lines may have a UTF-8 replacement glyph at a page boundary, affecting only preview. Repair/recovery of interrupted logs is outside this phase. Complete log copy remains in the existing live Experiment console; archived Logs copies only a selected bounded page.

**Validation.** New pure reader and Tk UI tests, inherited stage-1 test update, fresh-archive identity, exact-parent binary patch and frozen-code checks. Windows hardware validation remains outstanding.
