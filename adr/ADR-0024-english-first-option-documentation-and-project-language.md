# ADR-0024 — English-first option documentation and project terminology (v0.2.5)

**Context:** The working GUI must scale beyond seven initial demos. Documentation previously described parameters but rarely explained individual discrete values.

**Decision:** Rename visible starter-demo actions and selection labels to project terminology, without renaming technical source repositories, internal demo keys, profiles or run formats. Treat the English manual as the editorial baseline for new option-level descriptions. Extend English overlay records with explicit `options: [{value, description}]` where a field has enumerated or documented discrete choices. Render the new options in both the English Markdown manual and the English in-app Manual pane. Polish reference documentation remains unchanged this iteration.

**Alternatives rejected:** Renaming internal persisted identifiers, inventing UI controls for ioHub-only settings, changing the Polish manual without reviewed translations, or duplicating option descriptions in two independent hand-written places.

**Impact:** No new packages, background jobs, disk scanning, experiment behavior or persistence migration. English Manual uses the same existing cached help JSON as the tooltip system and does not write to configurations.

**Open:** Translate the new English options into Polish in a dedicated future iteration after terminology review. Independently validate hardware-specific option semantics on target systems.
