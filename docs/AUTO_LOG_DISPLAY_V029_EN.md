# v0.2.9 — optional automatic experiment log display (EN)

## Scope

On **Experiment → Launch**, a new **Auto-show logs** toggle sits next to **Show Logs**. The toggle defaults to **ON** and is stored only in the local application `settings.json`, not in project profiles, YAML or PsychoPy options.

- **ON (default):** starting a run automatically opens the existing Experiment log window. The on-screen preview is bounded to the latest 2,000 lines / 256 KiB (whichever is reached first).
- **OFF:** starting a run does not create a log window or update a Tk text widget. Subprocess execution, logging and final archives continue unchanged. **Show Logs** still opens the recent preview on demand and updates it while open; toggling OFF also closes a visible log viewer.
- During a run, the complete ordered GUI log is held in a `SpooledTemporaryFile` (256 KiB in RAM, then an OS temporary file). Following the final status, the full untruncated `experiment_<timestamp>_<ID>.log` is written in the project execution folder. The runner's existing separate `console_*.log` is still finalized after child exit.
- **Copy entire log** accesses the complete spool/archive only when the user requests it. Display limits do not truncate that operation.

## Limitations

Excessive subprocess output still incurs process and event-queue overhead; the toggle removes automatic rendering and bounds Tk's live preview history, not PsychoPy's production of log messages. A complete GUI log requires the GUI to receive the final event. Disk-full or temporary spool failures can affect logging but should not terminate the running experiment.

**Unchanged:** native launcher, validation, measurement/output-ID binding, projects, YAML, manual, GUI palette inherited from v0.2.6.
