# GUI Settings — option reference

This guide documents **pytracker-gui interface settings only**. It does not change experiment configuration or upstream repository data. Open the blue `i` icon beside an option for a concise explanation, then `man` to locate the relevant section here.

**Reading the controls:** gray labels show options; blue `i` icons provide help; orange headings mark major topics, and green monospace text highlights literal configuration values. All values described as read-only are managed elsewhere.

## Window & appearance

Window preset and fixed Home tile dimensions. The saved size is used at the next launch; it is not applied immediately.

## Option: window_size

Select one of the available window-size presets. A smaller display can constrain the resulting window to its usable area. The selection is not permanent until you choose **Save window size**.

## Option: save

Save the currently selected window preset. The saved size is used on the next application launch, not immediately.

## Option: tile_size

The four Home tile images are always **546 × 365 pixels** each. They do not stretch or resample when the window is resized; scrollbars appear if needed.

## Option: paths

Paths shown here are read-only snapshots. Change supported repository and interpreter paths under **Experiment → Environment**; this page does not move or rewrite any directory.

## Option: gui_home

Directory for GUI-owned configuration and state, separate from experiment measurements and original repository files.

## Option: projects_root

Parent directory for user projects, saved profiles, run directories and their execution history. Do not delete it when upgrading the GUI.

## Option: demo_root

Root of the supplied starter-project/examples repository, used for selecting demonstration configurations; it is not the user-project history directory.

## Option: upstream_root

Root of the original upstream framework checkout used by the experiment runtime, not the GUI or demo repository.

## Option: python

Configured Python interpreter for experiment launches. This read-only display does not check whether PsychoPy, ioHub or a physical eye tracker works.

## Option: preferences

Status-only summary of current preferences. The underlying controls live elsewhere in the application.

## Option: language

Current language for GUI labels and menus. This is separate from experiment stimulus languages.

## Option: help_language

Current language for parameter descriptions and their detailed manual entries. It is independent of the GUI label language.

## Option: auto_logs

Shows whether the live console Logs view opens automatically during experiment execution. Disable it in Experiment if you prefer to open Logs manually; it does not disable journal capture.

## Option: journal

Each run has a single incremental console journal: an active or incomplete `.log.part`, or a completed `.log`. These logs contain console output, not gaze measurement samples.

## Option: colors

The editor changes only the existing GUI palette and supported icon tint. Enter six-digit colors in `#RRGGBB` format. Preview swatches are not a live preview of the entire GUI.

## Option: save_colors

Validate every palette entry before saving. Invalid colors reject the whole save; accepted settings take effect when the GUI is restarted.

## Option: reset_colors

Replace the edit fields with factory colors without saving them. To persist the reset, click **Save colors** and restart.

## Option: ICON_COLOR

Tint applied to supported inactive interface icons. Selected navigation icons may intentionally retain their orange active state; some pre-rendered artwork does not use this setting.

## Option: window

**Main application window background.** Enter a six-digit RGB value in `#RRGGBB` format. **Save colors** validates the whole palette; restart the GUI to apply the saved color. Some assets and active-state icons use fixed artwork or a separate style.

## Option: surface

**Background of primary content panels.** Enter a six-digit RGB value in `#RRGGBB` format. **Save colors** validates the whole palette; restart the GUI to apply the saved color. Some assets and active-state icons use fixed artwork or a separate style.

## Option: surface_alt

**Secondary panel and popover background.** Enter a six-digit RGB value in `#RRGGBB` format. **Save colors** validates the whole palette; restart the GUI to apply the saved color. Some assets and active-state icons use fixed artwork or a separate style.

## Option: field

**Input fields and inset content areas.** Enter a six-digit RGB value in `#RRGGBB` format. **Save colors** validates the whole palette; restart the GUI to apply the saved color. Some assets and active-state icons use fixed artwork or a separate style.

## Option: hover

**Hover-state background where the theme supports it.** Enter a six-digit RGB value in `#RRGGBB` format. **Save colors** validates the whole palette; restart the GUI to apply the saved color. Some assets and active-state icons use fixed artwork or a separate style.

## Option: border

**Panel and control outlines.** Enter a six-digit RGB value in `#RRGGBB` format. **Save colors** validates the whole palette; restart the GUI to apply the saved color. Some assets and active-state icons use fixed artwork or a separate style.

## Option: text

**Primary text.** Enter a six-digit RGB value in `#RRGGBB` format. **Save colors** validates the whole palette; restart the GUI to apply the saved color. Some assets and active-state icons use fixed artwork or a separate style.

## Option: muted

**Secondary and less prominent text.** Enter a six-digit RGB value in `#RRGGBB` format. **Save colors** validates the whole palette; restart the GUI to apply the saved color. Some assets and active-state icons use fixed artwork or a separate style.

## Option: accent

**Primary orange accent for emphasis and selected controls.** Enter a six-digit RGB value in `#RRGGBB` format. **Save colors** validates the whole palette; restart the GUI to apply the saved color. Some assets and active-state icons use fixed artwork or a separate style.

## Option: accent_hover

**Hover shade of the accent color.** Enter a six-digit RGB value in `#RRGGBB` format. **Save colors** validates the whole palette; restart the GUI to apply the saved color. Some assets and active-state icons use fixed artwork or a separate style.

## Option: accent_text

**Text drawn on an accent-colored background.** Enter a six-digit RGB value in `#RRGGBB` format. **Save colors** validates the whole palette; restart the GUI to apply the saved color. Some assets and active-state icons use fixed artwork or a separate style.

## Option: selection

**Selection highlight in supported controls.** Enter a six-digit RGB value in `#RRGGBB` format. **Save colors** validates the whole palette; restart the GUI to apply the saved color. Some assets and active-state icons use fixed artwork or a separate style.

## Option: success

**Positive status indicators.** Enter a six-digit RGB value in `#RRGGBB` format. **Save colors** validates the whole palette; restart the GUI to apply the saved color. Some assets and active-state icons use fixed artwork or a separate style.

## Save and reset behavior

**Save window size** applies on the next start. **Save colors** validates every color before saving; the active theme remains unchanged until restart. **Restore defaults** only fills the palette editor with factory values; use Save colors to persist the reset. These controls do not modify experiments.
