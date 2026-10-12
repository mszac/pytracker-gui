# v0.2.6 — Manual: Index and Documentation

The **Manual** screen opens **Index** by default, preserving the original
searchable catalogue of 87 parameters and their extended descriptions. Every
`man` link in contextual tooltips still opens the corresponding **Index** entry,
even after visiting another tab.

In the English Index, selectable option *values* under **Available options** now
appear in green, while the heading keeps its muted heading color. No value,
parameter description, configuration, or selection behavior has been changed.

The new **Documentation** tab browses local `*.rst` files from the original
`<tobii-pytracker>/docs/` checkout, including nested directories. It intentionally
excludes `tobii-pytracker-demo`. Filter by file path and select a document to read
its original reStructuredText source with lightweight heading highlighting.
This is not a full Sphinx renderer: advanced directives, cross-references,
figures and substitutions remain visible as source text.

The file list is scanned only on first opening Documentation (or after an
upstream-path change when that tab is revisited); file contents are read only when
selected. The viewer never writes to source files and needs no network,
background worker, external GUI library or new runtime dependency. Missing
`.rst` files produce a clear message. Files above 2 MiB are rejected by the
viewer rather than loading unusually large content into Tk.

Experiment processes, YAML editing, project folders, logs and other screens are
unchanged.
