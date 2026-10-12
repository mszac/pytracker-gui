# v0.2.10 — Manual: starter-project documentation tree

This iteration derives **directly from v0.2.9** and retains the v0.2.6 visual palette, project storage and experiment-launch contracts.

## Navigation

- Removed **Diagnostics** from the top-level navigation and dashboard. Existing environment and configuration checks within Experiment remain unchanged.
- Manual now has three tabs: **Index** (default), **Documentation** (local upstream `tobii-pytracker/docs/*.rst`) and **Demo Project Documentation** (local Markdown from `tobii-pytracker-demo`).
- The third tab provides an expandable tree: project name → its Markdown instruction files. A matching optional `docs/basic_examples` guide is shown under the corresponding project without copying or rewriting the source file.
- Tooltip `man` links still open the matching parameter in the **Index** tab. Navigation never commits unsaved YAML.

## Performance and safety

The additional browser is created lazily. Its file inventory is read only when the user first enters the tab or changes the demo-repository location, and a document is read **only when selected**. There is no external renderer, web engine, network call, subprocess, polling or new dependency. Files are read-only, symlinks/out-of-repository paths are rejected, and Markdown files larger than 1 MiB are not opened.

A deliberately small native `tk.Text` renderer styles Markdown headings, bullets, emphasis, quotes and code blocks and common RST headings, lists and code. **It is not full CommonMark/Sphinx/HTML**. Complex tables, images, directives and links may remain simplified. Documents larger than 256 KiB bypass per-line formatting to keep interaction responsive.

Analysis output, participant CSV data and run logs are excluded. Physical Windows/PsychoPy/Tobii execution remains an external validation gate.
