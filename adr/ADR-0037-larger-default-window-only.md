# ADR-0037 — Initial window dimensions only

Date: 2026-10-12

Decision: Accept the user's exact-scale Windows screenshot as the target **application content** dimension (1429 × 1097 px). Replace only the `AppShell` maximum initial geometry values 1300/960 with 1429/1097; retain the same `screen_width/height - 90` guard, minimum dimensions, native window resizing and every control layout. No new screen behavior or feature is introduced.

Rationale: a larger initial frame improves visibility after the addition of several controls without perturbing existing panel sizes, saved state, or the four fixed-size dashboard images. Do not change independent `PytrackerGUI` initialization geometry because AppShell remains the final, authoritative application-window setter.
