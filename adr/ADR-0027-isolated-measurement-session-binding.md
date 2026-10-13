# ADR-0027 — run-ID-scoped measurement output and fail-closed validation

**Context:** The previous launcher used validators selecting recent measurement sessions by mtime under a shared `output.folder`. Five-character IDs in GUI log paths did not identify the exact external `data.csv`; concurrent or near-time runs could be misattributed.

**Decision:** Keep upstream untouched, reserve a unique output root per GUI run/block under the user's existing configured output, inject that exact path only into the run-specific YAML snapshot, and locate exactly one upstream-created session under that root. Use explicit `--session` when supported, otherwise pass only the private singleton root to Test Demo. Persist the exact binding or an unresolved reason in `result.json`. Reject validation PASS when the exact association is missing.

**Alternatives rejected:** `newest()` or mtime matching, modifying upstream CSV format, moving CSV into `projects/`, patching demo validators, appending one common ID to a shared unisolated output folder.

**Tradeoff:** One additional lightweight output-directory level per block and schema-2 run manifests. Preexisting v0.2.6 run manifests remain historical; only new v0.2.8 launches use the contract. The original project output base remains unchanged, and the GUI's in-memory YAML and saved profile are not rewritten. Unrelated log-buffer changes are deliberately deferred.
