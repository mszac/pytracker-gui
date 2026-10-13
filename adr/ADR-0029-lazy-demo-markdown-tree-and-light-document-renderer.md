# ADR-0029 — Lazy demo Markdown tree and bounded local formatting

**Status:** accepted for v0.2.10. **Parent:** exact v0.2.9.

**Need:** remove unused Diagnostics top-level destination; keep Manual Index/deep links intact; expose separate markdown instructions from individual starter projects and improve RST/Markdown readability without changing experiment runtime.

**Decision:** remove the Diagnostics navigation route and tile only; add an independently lazy `DemoProjectDocsBrowser` tab containing a native `ttk.Treeview` grouped by each discovered `examples/<project>/` directory. Optionally attach a matching `docs/basic_examples` guide to the same project. Do not mix in upstream `docs/*.rst`, `output/`, `projects/`, or user measurement data. Files are opened on selection only, with local-path and size checks. Share bounded style-only document rendering between this browser and the existing RST browser; no Sphinx/Markdown runtime, HTML viewer, filesystem watcher, threading, or subprocess.

**Rejected:** a web engine, full markdown/RST parser dependency, eager reading of every document, and migrating documentation into pytracker-gui. Large documents fall back to unstyled text instead of blocking Tk on thousands of styled line insertions.

**Invariants:** Index is default; tooltip `man` always selects Index; no YAML commits on navigation; no modifications to launcher, adapters, log storage, device configuration, project format, theme, or underlying repositories.
