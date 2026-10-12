# Dashboard: fixed image tiles (v0.2.18)

Scope: Only the Home dashboard reached through the `pytracker-gui` brand in the top-left corner.

- Four existing destinations remain exactly Experiment, Logs, Statistics, Manual. The buttons use the four user-selected labelled images, not generated substitutes.
- Images are offline-optimized, RGB PNGs with a fixed resolution of **546 × 365 pixels**; each occupies around 200–220 KiB, versus 1.8–2 MB for its input. The labels in the supplied artwork remain in English for both interface locales; button metadata remains localized for keyboard/accessibility and existing tests.
- Image-backed native ttk buttons do not change size in response to enlarging or shrinking the window. An event-driven native Canvas viewport offers horizontal/vertical scrollbars only if a smaller window cannot fit the fixed 2×2 grid. Normal startup needs neither scrollbar.
- Assets are loaded once when Home is first opened, with no background processing or runtime Pillow dependency. Image resizing/cropping is done only at build time.
- No change to child-screen logic, Experiment, PsychoPy, YAML, projects, Logs, Manual, statistics, global theme, settings, or persistence.

Verification: measure all four tile sizes before/after resize; test scrollbar appearance/disappearance, previous click routing and localization metadata; verify the immutable originals in the parent release and the packaged PNG sizes; smoke-test both Full and Commit Ready packages on an extracted tree.
