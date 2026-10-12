# v0.2.8 — exact GUI run ID to measurement session binding

## Contract

Every new GUI execution retains its case-sensitive five-character run ID and project history folder `projects/<project>/experiments/<YYYYMMDD_HHMMSS>_<ID>/`. The original upstream PsychoPy code still generates the timestamped measurement session folder and writes `data.csv` and companion measurement files.

For each block, the per-execution YAML snapshot now points `output.folder` to a uniquely reserved child of the user-configured output root:

```text
<user_configured_output.folder>/
  pytracker_<YYYYMMDD_HHMMSS>_<ID>_<block>/
    <upstream_timestamped_session>/
      data.csv
      ... native measurement files ...
```

Reusable project profiles and original source YAML are unchanged. Machine/PV blocks have independent roots. This contract applies to new v0.2.8 launches only; it does not migrate older measurements.

## Deterministic binding

- The new root is created exclusively before launching the child; a collision fails instead of silently reusing data.
- After each block exits, only that reserved root is inspected. Exactly one immediate child directory containing `data.csv` is accepted. Zero or multiple candidates are explicitly **unresolved**. Symlinks are ignored.
- Validators for UX, Text Search, Image Semantic and Time Series receive the exact `--session` path. The original Test Demo validator has no `--session` argument: it receives only the already checked single-session `--output-root`. No timestamp/mtime selection across shared output is used.
- `run.json` (schema 2) records the ID and configured/reserved roots; `result.json` includes `measurement_sessions` by block with `linked/unresolved`, exact session and CSV path, data file size or the reason for failure.
- A validator cannot produce a `COLLECTION VALIDATED` status unless a unique CSV binding also exists. This ties provenance to a file; data completeness and eye tracker fidelity remain separate validation concerns.

## Cost, limits, and Windows gate

There is no new worker, timer, polling loop or global output scan. Root reservation happens prelaunch; association and result metadata are written post-block. Source output data are not modified. External later moves/deletes of `data.csv` can invalidate a historical path in the metadata.

Log buffering remains unchanged in v0.2.8. For a subsequent iteration, recommend 256 KiB **and** 2,000 lines (whichever comes first) for the live GUI preview only, while keeping complete diagnostics in the existing spool/archival workflow. The current `SpooledTemporaryFile` uses a 256 KiB in-memory threshold, then OS temporary storage.

On physical Windows, run Test Demo MouseGaze, UX and two Time-Series blocks. Check the unique ID in the output path, `run.json`, `result.json` and both experiment log filenames. Repeated runs must not share a measurement root.
