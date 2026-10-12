# v0.2.4 — Manual screen and logo

## Scope

- The clickable pytracker-gui logo at the top-left is now placed on a white circular background; the old orange diamond ◈ has been removed. Clicking the logo or product name still opens the Dashboard.
- Top navigation and the Dashboard now contain a **Manual** entry. It is a separate, lazily constructed view created only when first opened, without timers, extra processes or experiment data reads.
- The Manual covers **87 existing parameters**. Entries can be searched by name, ID, description and group. Selecting an entry displays its short and extended descriptions and availability status.
- Tooltips opened using the `i` icon contain an orange **man** link. Clicking it opens the matching Manual entry without changing forms or committing edited YAML.
- Manual text is read from the existing PL/EN catalogs (`parameter_help.json` and `parameter_help_en.json`). The documentation content follows the independently selected help language; navigation follows the GUI language.

## Boundaries

The seven demo variants, PsychoPy launcher, gaze selection, project and session storage, profiles, YAML configuration, run logs, and safeguards for unsaved edits are unchanged. Extended descriptions are not downloaded or recomputed in the background. The Manual is read-only.

## Validation

Linux/Xvfb host tests cover lazy Manual construction and reuse, exact deep-link navigation via `man`, Polish/English long descriptions, search, Dashboard tiles and preserving unsaved invalid YAML. Windows/HiDPI and physical Tobii testing remain external gates.
