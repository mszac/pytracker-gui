# v0.2.19 — Larger initial application window

This update changes only the initial window dimensions. From the user's 1:1 Windows screenshot, the application client area (excluding the OS title bar and frame) measures approximately **1429 × 1097 pixels**. On screens with sufficient available area, pytracker-gui now opens at that size rather than the previous **1300 × 960** cap.

The previous screen-margin and small-display guards remain in force: the requested size is capped by screen width/height minus 90 pixels with the established minima of 940 × 650. The user can still resize the window manually.

No navigation layout, panel dimensions, images, styles, controls, initial selection, experiments, logs, YAML or other runtime behavior is changed. The four Home image tiles remain fixed-size. Physical Windows/HiDPI visual confirmation remains a user-machine check.
