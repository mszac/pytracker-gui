# v0.2.11 — Demo documentation tree contrast (EN)

This patch only affects the left-side tree in **Manual → Demo Project Documentation**. On Windows, `ttk.Treeview` displayed a light background with light text because the global theme configured an unused `TTreeview` style rather than the actual `Treeview` base style.

A scoped `DemoDocs.Treeview` style now explicitly sets a dark field background (`#161e26`), light text (`#f2f5f9`), and orange selection (`#ff8931`) with dark selected text. No global palette, geometry, Markdown/RST rendering or other functionality is changed. Regression coverage checks normal and selected rows.

Physical Windows verification remains open: inspect contrast for project groups, filenames, and selection, including after reopening the tab.
