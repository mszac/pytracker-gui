# GUI Documentation tab — v0.2.17

The **Manual → GUI Documentation** tab displays documentation belonging to the installed **pytracker-gui** project itself. It does not browse the upstream `tobii-pytracker` engine or the `tobii-pytracker-demo` repository: those remain available in the separate **Documentation** and **Demo Project Documentation** tabs.

The left-hand tree groups current guides and selected feature guides under **English** and **Polski**. A selected `.md` file appears in the right-hand read-only viewer using the same lightweight native Tk text formatting already employed by the other Manual documentation tabs. The tree contains an explicit list of bundled documents; historical ADRs, archived development logs, project experiment data and arbitrary user files are excluded.

The index is prepared only when opening this tab. Document content is loaded only when selecting a file; each read is bounded to 1 MiB and large files receive the existing plain-text fallback. No browser engine, network, extra dependencies, background scanning, subprocesses, timers or write-back are introduced. The `man` tooltip links continue opening the 87-parameter **Index** tab. Switching tabs does not commit unsaved YAML.

In **Experiment → Environment**, only the horizontal stretch of **Save paths**, **Check Python**, **Load repository** and **Detect layout** is changed: all four occupy their grid column's natural maximum width (determined by Load repository in the English interface). Their original natural height, icons, text, commands, colors, spacing and button styles remain untouched; the classic one-row editor footer and movable panel separators are preserved.

This release does not modify PsychoPy execution, experiment data, YAML persistence, run snapshots, journaling, the Logs screen or the global theme. The user guides and documentation indexes are updated in English and Polish to include the fourth Manual tab.
