# pytracker-gui — parameter reference (M1)

> Updated: 2026-10-11, v0.2.5. English is the baseline for new option-level documentation.
> Descriptions cover the known contracts of
> `sbobek/tobii-pytracker`, `mszac/tobii-pytracker-demo`
> (v1.17.0 demo set), and the pytracker-gui configuration editor.
> This is not evidence of hardware execution or a guarantee about newer
> upstream commits whose identities have not been pinned.

All **87 parameters** provide a one-sentence tooltip and an extended
explanation. YAML and CLI identifiers are deliberately not translated.
**The `gui` status means an editor field or stored preference, not that
an experiment has completed or collected data have been validated.**
Saving a profile or exporting YAML does not launch PsychoPy; use Launch project.
The `yaml-only`, `iohub-only`, `reference` and `future` categories
may lack dedicated editors or complete execution support.

Where an item offers discrete choices, the **Available options** section documents each supported or documented value and its effect.
The in-app Manual screen uses this English catalogue as its primary content source; the Polish text remains an independent translation.
Polish edition: [`PARAMETER_MANUAL_PL.md`](PARAMETER_MANUAL_PL.md).

**Sources:** [upstream](https://github.com/sbobek/tobii-pytracker), [demo repository](https://github.com/mszac/tobii-pytracker-demo), [MouseGaze YAML](https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml), [Tobii YAML](https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/eyetracker_config.yaml).

## Environment / GUI

### `gui.demo_root` — Starter-project repository root

**In brief:** The nested repository of supplied starter projects containing examples/ and tools/.

**Details:** Choose the checked-out `tobii-pytracker/tobii-pytracker-demo` directory, which currently provides the seven supported starter variants and their adapters. This is the path to the upstream examples source repository, not the storage directory for your individual research projects. Personal projects and execution histories are stored separately in `tobii-pytracker/projects/<name>/`; changing this field does not move those projects.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/mszac/tobii-pytracker-demo

### `gui.upstream_root` — Upstream repository root

**In brief:** Root directory of the cloned sbobek/tobii-pytracker repository.

**Details:** Select the original `tobii-pytracker` root with `pyproject.toml`, `src/tobii_pytracker`, and `configs/`. The demo repository and `pytracker-gui` should be separate child directories in that checkout. The layout preflight inspects files and locations without modifying upstream source code.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#usage

### `gui.python` — Python interpreter

**In brief:** Path to the Python 3.10 executable in the existing pytracker-env.

**Details:** Select the Python executable within the existing `pytracker-env` Conda environment instead of an unrelated system interpreter. The upstream project documents Python 3.10.x as a requirement. The GUI probes interpreter details only; it does not prove that PsychoPy, ioHub, or a tracker can run.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#usage

### `gui.variant` — Starter project selection

**In brief:** Choose a starter project configuration supplied with the examples repository.

**Details:** Select one of seven supplied starter project variants as the working configuration for this GUI. The choice determines which original YAML file or files are loaded; it does not rename, create, or overwrite the user-owned project directory. Actual execution occurs only after using the Launch project control. The seven supplied entries are starting points, not a limit on future project types.

**Available options:**

- `test_en` — Test Demo [EN]: image classification with three supplied image trials; standard upstream execution path.
- `ux_en` — UX A/B Text [EN]: twelve English text-layout tasks using the bundled text adapter.
- `ux_pl` — UX A/B Text [PL]: Polish text-layout variant with its own YAML.
- `ts_machine_pv` — Time-Series Noise [Machine → PV]: two successive nine-trial blocks, each with separate YAML and output validation.
- `search_en` — Text Search [EN]: English text-search tasks using the text adapter.
- `search_pl` — Text Search [PL]: Polish text-search tasks using the text adapter.
- `image_en` — Image Semantic [EN]: semantic image tasks using the image adapter.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/mszac/tobii-pytracker-demo

### `gui.block` — Project configuration block

**In brief:** Select the configuration block within the chosen starter project.

**Details:** Most supplied starter projects have one main configuration block. Time-Series Noise contains two distinct blocks (Machine Vibration and PV Power) with separate YAML files and trial limits; on launch they are run sequentially. Switching blocks changes only the configuration being edited and does not start or stop a running session.

**Available options:**

- `main` — The sole configuration block of most starter projects; edit and launch it as a single unit.
- `machine` — First Time-Series Noise block (Machine Vibration); stores its own YAML and executes before PV.
- `pv` — Second Time-Series Noise block (PV Power); executes only after Machine completes successfully.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/mszac/tobii-pytracker-demo

### `gui.gaze` — Gaze recording mode

**In brief:** Choose between no gaze acquisition, the MouseGaze emulator, and a physical Tobii tracker.

**Details:** The gaze mode is a run-time project setting, not a keyboard/mouse input lock. NO_GAZE skips gaze acquisition while leaving mouse-based answers available, MOUSEGAZE emulates tracker samples using ioHub, and TOBII expects a supported hardware device. The launcher passes this selection to the isolated native process; actual gaze recording still depends on PsychoPy/ioHub and device readiness.

**Available options:**

- `NO_GAZE` — Do not initialize gaze acquisition; mouse answers in PsychoPy can still be used. The current upstream entry point still reads an ioHub YAML file.
- `MOUSEGAZE` — Use the PsychoPy ioHub mouse eye-tracker emulator. With the supplied configuration, the right mouse button controls simulated gaze reporting.
- `TOBII` — Use a supported connected Tobii device and its own ioHub configuration; success depends on the driver and hardware being available.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#usage

### `gui.iohub_yaml` — ioHub configuration file

**In brief:** Selects the configuration file for the simulated or physical eye tracker.

**Details:** For MouseGaze the default path is generally `configs/mouse_eyetracker_config.yaml`; for Tobii it is `configs/eyetracker_config.yaml` under upstream. The original entry point reads this file even when the tracker is disabled, so NO_GAZE should also reference an existing YAML. This GUI edits the file path, not ioHub settings inside the file.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#usage

### `gui.yaml_editor` — YAML editor

**In brief:** Edits a working YAML copy, including fields outside the forms.

**Details:** The raw YAML tab edits a working copy, including keys not exposed by the form. `ruamel.yaml` preserves comments and unknown fields through typical round-trips but does not promise byte-for-byte formatting identity. Apply changes into the in-memory model first and explicitly save a profile or export a YAML copy.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/mszac/tobii-pytracker-demo

### `gui.profile` — Saved project profile

**In brief:** Preserves the current working configuration in the selected project.

**Details:** Saving a profile writes current editable YAML and runtime choices inside the active project under `projects/<project-name>/profiles/`, without modifying the original examples repository. The project also retains its global preferences and independent execution history under `experiments/`. Saving does not start PsychoPy, and external data paths still need to exist when a copied project is opened elsewhere.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/mszac/tobii-pytracker-demo

### `gui.instructions` — Experiment instructions

**In brief:** Text displayed on the experiment's introduction and completion screens.

**Details:** The upstream `instructions.intro` and `instructions.outro` values are lists of participant-facing text. Each line in the GUI form corresponds to an element of the YAML list. Keep wording consistent with the selected demo task and actual input method, particularly when gaze mode changes.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

## Dataset / output

### `dataset.image.path` — Image directory

**In brief:** Path to the image directory, typically containing category subdirectories.

**Details:** The image modality reads files in supported formats such as JPEG and PNG from the selected directory. Category subdirectories can provide class labels in image-based examples. Relative paths in the supplied demos are interpreted against the demo repository root; this editor checks paths but does not load an experiment.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.image.bbox_model` — Image bounding-box model

**In brief:** Selects image regions via grid, superpixel or saliency.

**Details:** This setting selects how spatial regions may be defined on an image for associating gaze with stimulus locations. `grid` divides the image into regular cells, `superpixel` applies segmentation, and `saliency` uses an importance map. It does not run an image model in the GUI; actual availability and cost depend on runtime dependencies.

**Available options:**

- `grid` — Divide the image into a regular grid of rectangular regions; deterministic spatial partitioning without image-content segmentation.
- `superpixel` — Segment the image into locally similar regions and derive bounding regions from those segments; results depend on image content.
- `saliency` — Use a saliency-based importance map to locate visually prominent image regions; depends on the applicable model implementation.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.path` — Text dataset file

**In brief:** Path to a CSV file containing text tasks and their data columns.

**Details:** Select a CSV file with a header row and the columns named by `label_column_name` and `text_column_name`. Demo-specific adapters may rely on additional fields. Static validation can check the file and expected headers, but it does not execute the trial renderer.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.label_column_name` — Text label column

**In brief:** Name of the CSV column containing labels or correct classes.

**Details:** Enter the exact CSV header, including capitalization, used to identify a text task label or class. This is a reference to an existing column, not a new generated field. A missing or mismatched header prevents the dataset from being interpreted as intended.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.text_column_name` — Text content column

**In brief:** Name of the CSV column containing text shown to participants.

**Details:** This is the existing CSV column holding the text displayed as a stimulus. It serves a different purpose from the label column and should not be interchanged with it. The GUI does not rewrite the dataset when this reference changes.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.bbox_model` — Text bounding-box model

**In brief:** Sets the text region granularity to word, line, or sentence.

**Details:** The selected text region model sets the granularity of gaze-related regions: `word`, `line`, or `sentence`. This can affect the interpretation of fixations over text later in the workflow. It does not modify the original CSV content.

**Available options:**

- `word` — Use each individual word as the gaze-analysis region.
- `line` — Group rendered text into individual line-level regions when linking gaze to the displayed text.
- `sentence` — Group text into sentence-level regions; a sentence can span several visual lines.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.color` — Text color

**In brief:** Color of the characters in PsychoPy text stimuli.

**Details:** The general upstream text dataset configuration exposes an optional stimulus foreground color. Use a value accepted by the applicable PsychoPy renderer and keep enough contrast with `background_color`. The form does not automatically add this optional key to demos that lack it.

**Availability:** `yaml-only` — YAML only; no dedicated form field

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.background_color` — Text background color

**In brief:** Background color of the text stimulus.

**Details:** This sets the background of a textual stimulus in the general upstream configuration. Choose a contrasting value relative to `dataset.text.color`. Demo-specific adapters may apply additional styling, so inspect the relevant renderer before relying on an appearance change.

**Availability:** `yaml-only` — YAML only; no dedicated form field

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.font_height` — Text font height

**In brief:** Font height used for text stimuli in the demo adapters.

**Details:** Selected text demos define the size of rendered stimulus characters through this extra YAML field. Changes can alter line wrapping and the placement of gaze regions. It is demo-specific and is not guaranteed to exist in all upstream text configurations.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/mszac/tobii-pytracker-demo

### `dataset.text.wrap_fraction` — Text wrapping width

**In brief:** Fraction of display width available for demo text wrapping.

**Details:** In selected demo adapters, a positive value no greater than one specifies the fraction of display width available for text layout. Narrower text can wrap into more lines and change gaze-region geometry. This is a demo extension rather than a universal upstream YAML setting.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/mszac/tobii-pytracker-demo

### `dataset.time_series.path` — Time-series dataset file

**In brief:** Path to a CSV file containing time-series samples and classes.

**Details:** Select the CSV containing tabular time-series observations and the required label header. The Time-Series Noise demo has separate Machine and PV configurations, which may reference different datasets. Static path checks do not validate downstream time-series visualizations or acquisition.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.time_series.label_column_name` — Time-series label column

**In brief:** CSV header identifying each time-series class.

**Details:** Name the existing CSV header used as a class or label for time-series observations. The value must match the actual file header. Changing it does not alter or preprocess the signal data.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.time_series.bbox_model` — Time-series bounding-box model

**In brief:** Selects time-series region boundaries: sample or window.

**Details:** The `sample` strategy associates regions with individual samples, while `window` groups adjacent observations into regions. The choice affects how gaze over a plotted series may be interpreted. Its effective behavior belongs to the upstream model and trial renderer, not the GUI editor.

**Available options:**

- `sample` — Use individual plotted samples as regions for linking gaze to time-series positions.
- `window` — Group neighboring time-series samples into larger analysis windows.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `output.folder` — Output folder

**In brief:** Destination directory for experiment result files.

**Details:** This is the destination for result files produced by the research runtime, such as session CSV files. A relative path is resolved against the example repository working directory when using the existing launcher. It is not the separate project history directory (`projects/<name>/experiments/`), which stores GUI-generated run manifests and console logs; the GUI does not move research results into that history directory.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `bbox_model.folder` — Custom bounding-box model folder

**In brief:** Directory containing an optional custom region detection model.

**Details:** The optional custom bounding-box model mechanism allows external code to supply regions when built-in strategies are insufficient. The folder must contain importable Python code compatible with the expected custom-model interface. The current GUI documents this YAML property but does not run or validate external model code.

**Availability:** `yaml-only` — YAML only; no dedicated form field

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `bbox_model.module` — Custom bounding-box model module

**In brief:** Python module exposing the custom region detection model.

**Details:** This names the Python module containing the custom model implementation. The interpreter that eventually launches the experiment must be able to import it. Editing the string does not install dependencies or test the import in this GUI.

**Availability:** `yaml-only` — YAML only; no dedicated form field

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `bbox_model.class` — Custom bounding-box model class

**In brief:** Python class implementing the custom bounding-box model.

**Details:** This specifies the Python class implementing the custom model contract, including methods such as `prepare_model`, `predict`, and `process`. A missing class or incompatible implementation can cause a runtime failure. This is an advanced YAML-only option, not an interactive model designer.

**Availability:** `yaml-only` — YAML only; no dedicated form field

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

## Monitor

### `display.monitor.name` — Monitor name

**In brief:** Name of the PsychoPy monitor profile.

**Details:** This is the identifier of the PsychoPy monitor profile used for stimulus geometry. It may interact with physical dimensions and display calibration. Use the intended workstation profile; the GUI does not test a physical monitor during configuration editing.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.monitor.resolution` — Monitor resolution

**In brief:** Stimulus display resolution in pixels as width and height.

**Details:** Enter the stimulus display width and height as an ordered pixel pair (for example `1920, 1080`). The value informs stimulus layout and coordinate calculations. It does not change the operating system display resolution; verify it against the real monitor.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.monitor.width` — Monitor physical width

**In brief:** Physical width of the active monitor area in centimeters.

**Details:** Supply the measured physical width of the active screen area in centimeters, not the diagonal size advertised in inches. Together with viewing distance it contributes to geometric and visual-angle conversions. Incorrect measurements can distort the mapping from pixels to visual angles.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.monitor.distance` — Viewing distance

**In brief:** Participant eye-to-screen distance in centimeters.

**Details:** This is the approximate distance in centimeters between the participant’s eyes and the display. PsychoPy can use it with screen width for visual-angle-related calculations. Use a value matching the research workstation rather than an arbitrary default.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.monitor.display_number` — Display number

**In brief:** Index of the display used by PsychoPy for the experiment.

**Details:** Screen numbering starts at zero and depends on how the operating system presents connected displays. On a multi-monitor station verify which screen actually receives PsychoPy stimuli. Editing the integer here does not independently check or rearrange physical monitors.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

## Appearance / layout

### `display.gui.button.size` — Response button size

**In brief:** Width and height of response buttons in pixels.

**Details:** Specify response button width and height as a two-number X/Y pair. Larger buttons change clickable targets and layout spacing. Assess the final appearance against display resolution and button margins in the actual demo renderer.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.button.margin` — Response button margin

**In brief:** Spacing between response buttons.

**Details:** This determines the spacing used around or between response buttons in the experiment layout. Too little space may make nearby responses harder to distinguish or select. Interpret the units and visual effect in the concrete renderer, not as a general desktop GUI setting.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.button.color` — Response button color

**In brief:** Background color of response buttons.

**Details:** Select the background color for answer buttons using a representation accepted by the relevant PsychoPy renderer. Maintain sufficient contrast with the button text color. This is a visual setting and does not change response values.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.button.text.color` — Response button text color

**In brief:** Color of the labels on response buttons.

**Details:** Set the foreground color of response labels, not the stimulus text itself. Ensure readability against `display.gui.button.color`. This setting does not change eye-tracker sampling or answer identifiers.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.button.text.size` — Response button font size

**In brief:** Font size of response-button labels.

**Details:** This setting controls the size of text rendered on the experiment response buttons. Large fonts or long labels may overflow a small button, so inspect the real PsychoPy window at the target display resolution. Changing the value in the configuration editor alone does not provide a graphical preview of the eventual response layout.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.fixation_dot.size` — Fixation dot size

**In brief:** Size of the fixation marker shown during the experiment.

**Details:** The fixation dot is a visual marker intended to guide a participant’s attention in applicable trials. This value controls its rendered size, not an eye-tracker measurement threshold. Whether and when it appears depends on the specific demo flow.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.fixation_dot.color` — Fixation dot color

**In brief:** Color of the gaze fixation marker.

**Details:** Choose a fixation marker color that remains clearly visible on the demo background. It is a stimulus appearance property and is unrelated to raw gaze precision. Do not confuse this marker with the separate ioHub calibration target.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.aoe` — Area of experiment

**In brief:** Size of the experiment layout area (AOE), not stimulus-specific AOIs.

**Details:** The upstream YAML defines this as a two-number size for the experiment layout area (AOE). It is not the same as per-stimulus Areas of Interest (AOIs) obtained from image, text, or time-series regions. Interpret its dimensions together with the actual PsychoPy layout and demo implementation.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `instructions.intro` — Introduction instructions

**In brief:** List of instruction lines shown before the experiment.

**Details:** Each line entered into the GUI is represented as one YAML list item. Describe the task, response controls, and start sequence in language appropriate to the participant. Check that the wording remains accurate if the gaze source is changed.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

### `instructions.outro` — Completion instructions

**In brief:** List of messages shown after the demo is completed.

**Details:** This list contains participant-facing text shown after the demo is complete. It may describe how to exit PsychoPy or what happens next. Displaying a completion message does not independently confirm that result files have been saved.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#configuration

## Launch parameters

### `runtime.config_file` — Experiment YAML configuration

**In brief:** The experiment configuration file passed to the original runtime.

**Details:** The original command-line interface accepts `--config_file` to load the experiment YAML. The GUI launcher instead snapshots the working YAML for the chosen starter project under the corresponding execution history directory and supplies it directly to upstream `CustomConfig` in a separate Python process. Relative dataset paths still use the examples repository as the working directory; saving a profile is a separate operation from launching.

**Availability:** `reference` — Upstream/CLI reference; not necessarily a dedicated editable field

**Source:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.eyetracker_config_file` — Eye-tracker configuration path

**In brief:** Path to the device YAML file consumed by ioHub.

**Details:** This upstream CLI option chooses the ioHub device configuration passed to the tracker subsystem. It should match the chosen MouseGaze or Tobii mode. The original entry point reads the file even when tracking is off, so selecting an existing path matters for NO_GAZE as well.

**Availability:** `reference` — Upstream/CLI reference; not necessarily a dedicated editable field

**Source:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.enable_eyetracker` — Enable eye-tracker

**In brief:** Enables ioHub gaze collection for MouseGaze or Tobii on launch.

**Details:** The `enable_eyetracker` value is True for MOUSEGAZE and TOBII and False for NO_GAZE. The ioHub YAML selects the actual device driver. Upstream still reads an ioHub configuration file when gaze is disabled; mouse-based responses remain available. The GUI forwards this setting to `main.main`, but device readiness is not guaranteed by static checks.

**Available options:**

- `True` — Start ioHub eye tracking and collect events using the chosen eye-tracker YAML and gaze mode.
- `False` — Skip tracker initialization; trial answers and other enabled channels may remain active.

**Availability:** `reference` — Upstream/CLI reference; not necessarily a dedicated editable field

**Source:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.enable_voice` — Voice recording

**In brief:** Passes the voice-recording preference to the launched experiment.

**Details:** The GUI forwards `enable_voice` to upstream `main.main`, including for demos that use runtime adapters. This mode requires an available microphone and functioning PsychoPy audio setup. Successful process startup does not prove an audio recording was saved; verify the files and behavior on the target Windows or Linux machine.

**Available options:**

- `True` — Request microphone recording; requires recording devices and working voice support in the selected runtime/adapter.
- `False` — Do not request microphone recording for the session.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.raw_data` — Raw gaze data

**In brief:** Passes the raw gaze recording preference to the eye-tracker runtime.

**Details:** The `raw_data` option is forwarded to the upstream runtime, including adapter-based demos. Raw gaze requires MOUSEGAZE or TOBII; the GUI rejects raw data with NO_GAZE. The exact data shape and completeness depend on the connected tracker and ioHub implementation, and require real-system validation.

**Available options:**

- `True` — Request full raw eye-tracker event data rather than the normal processed gaze samples; requires gaze acquisition.
- `False` — Use the regular gaze sample extraction path instead of raw-event output.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.disable_psychopy` — Headless mode

**In brief:** Runs in headless mode without opening a PsychoPy window.

**Details:** Upstream exposes this switch for a headless acquisition scenario without the regular PsychoPy experiment window. It is not equivalent to launching one of the seven current interactive demos. The M1 GUI intentionally does not expose this as an editable launch control.

**Available options:**

- `True` — Request headless operation without PsychoPy stimulus windows; upstream supports raw gaze/voice recording, but this GUI has not implemented a headless launch workflow.
- `False` — Run normal visible PsychoPy trials and response controls.

**Availability:** `future` — Upstream functionality deferred in the GUI

**Source:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.loop_count` — Trial count

**In brief:** Controls how many trials run in the selected demo block.

**Details:** The GUI passes the chosen trial count to `main.main` and constrains it to the audited maximum for each block. Time-Series Noise starts separate Machine and PV child processes, with up to nine trials each. With fewer than the standard number of trials, original fixed-length collection validators are skipped and collection remains explicitly unverified.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.log_level` — Log level

**In brief:** Controls the diagnostic verbosity of the launched experiment process.

**Details:** At launch, the GUI configures the original `CustomLogger` within the research Python subprocess with debug, info, warning, error, or critical. Captured stdout/stderr is persisted as `console.log` in an application-private run directory. More detailed logs aid diagnosis but do not replace collected-data validation.

**Available options:**

- `debug` — Show detailed diagnostic messages for troubleshooting and tracing runtime behavior.
- `info` — Show routine lifecycle messages and significant run events; normal recommended level.
- `warning` — Show warnings and more severe problems while suppressing routine informational messages.
- `error` — Show errors and critical failures only, suppressing warnings and lower-severity logging.
- `critical` — Show only the most severe failures; accepted by upstream CLI, though it may not be exposed by the current GUI selector.

**Availability:** `gui` — GUI field or preference; applied on launch where supported by this feature

**Source:** https://github.com/sbobek/tobii-pytracker#usage

## ioHub / eye tracker (documented only; currently not editable)

### `iohub.mouse.name` — Simulated tracker name

**In brief:** Name of the simulated device within the ioHub instance.

**Details:** The upstream MouseGaze YAML names its ioHub tracker device `tracker`. This identifier can be used when the program looks up the device through ioHub. Renaming it without corresponding changes in consumer code may prevent expected device lookup.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.mouse.auto_report_events` — Automatic event reporting

**In brief:** Controls whether MouseGaze reports events automatically.

**Details:** When false, reporting of events is not automatically started for the device and may require explicit activation by the client. The upstream example uses false. Changing it affects event collection timing and should be checked with the actual runtime.

**Available options:**

- `True` — Begin automatically reporting events when the device/experiment initializes.
- `False` — Do not report until event reporting is enabled explicitly (as the supplied MouseGaze configuration specifies).

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.common.save_events` — Save ioHub events

**In brief:** Controls whether ioHub saves gaze events.

**Details:** This switch controls saving events in the ioHub event store. It is independent from the experiment’s own CSV or other result export. Disabling it may prevent later inspection of certain event records.

**Available options:**

- `True` — Write supported ioHub device events to the ioHub event data store while recording.
- `False` — Do not store those events in the ioHub data store; this is separate from the experiment CSV.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.common.stream_events` — Stream ioHub events

**In brief:** Controls whether ioHub streams events to the experiment process.

**Details:** When true, ioHub can provide event samples to the consuming experiment as they arrive. Disabling this can interfere with online gaze processing. Streaming and saving are separate decisions.

**Available options:**

- `True` — Forward eye-tracker events to the experiment process while recording.
- `False` — Disable live event streaming to the experiment process; gaze-dependent tasks may then lack sample updates.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.common.event_buffer_length` — Event buffer length

**In brief:** Maximum number of events buffered by ioHub.

**Details:** This is the bounded size of an event buffer held by ioHub. A small buffer can cause old samples to be lost under load; an unnecessarily large one consumes more memory. The GUI does not benchmark or tune this value.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.common.monitor_event_types` — Monitored event types

**In brief:** Event types monitored or exposed by ioHub.

**Details:** This is the list of event types ioHub should monitor for a given tracker implementation. MouseGaze can expose simulated monocular gaze and other events, while the Tobii device uses its own binocular sample types. Do not copy lists blindly between different driver YAML files.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.enable` — Enable calibration

**In brief:** Enables calibration for the eye-tracking device managed by ioHub.

**Details:** Enables the driver-specific calibration flow where supported. A value shown in MouseGaze YAML does not guarantee identical behavior on Tobii hardware. This setting is documented only and is not exposed in the current GUI form.

**Available options:**

- `True` — Enable calibration when supported by the selected tracker driver.
- `False` — Skip the calibration routine if the driver allows it; accuracy can suffer without a valid previous calibration.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.type` — Calibration point pattern

**In brief:** Selects a THREE-, FIVE-, or NINE-point calibration.

**Details:** Selects the calibration point pattern, commonly the three-, five-, or nine-point options offered by the driver. More points may change time and spatial coverage, but available patterns are driver-specific. Verify the selected mode with the actual tracker.

**Available options:**

- `THREE_POINTS` — Calibrate at three target positions; the shortest listed pattern.
- `FIVE_POINTS` — Calibrate at five positions, offering additional spatial coverage.
- `NINE_POINTS` — Calibrate at nine positions for denser spatial coverage, requiring more time.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.randomize` — Randomize calibration order

**In brief:** Randomizes the order of calibration points.

**Details:** This toggles whether the presentation order of calibration positions is randomized. A false value generally follows a predefined order. Keep the choice consistent with the research procedure and supported driver.

**Available options:**

- `True` — Visit calibration target positions in a shuffled rather than fixed order.
- `False` — Use the configuration-defined calibration target order without shuffling the positions.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.auto_pace` — Automatic calibration pacing

**In brief:** Automatically advances between calibration points.

**Details:** Enables timed progression between calibration targets when the implementation supports it. If disabled, an operator or participant may need to advance manually. The exact behavior is defined by the ioHub driver, not by pytracker-gui.

**Available options:**

- `True` — Move automatically to the next calibration target after pacing_speed seconds.
- `False` — Require an operator/participant confirmation to advance; pacing_speed is ignored.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.pacing_speed` — Calibration pacing speed

**In brief:** Duration of each calibration point during automatic pacing.

**Details:** Specifies timing for automatic progression of calibration targets; the example configuration uses seconds. It may be irrelevant when automatic pacing is off. Too little display time may make steady fixation difficult.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.screen_background_color` — Calibration background color

**In brief:** Background color of the calibration screen.

**Details:** This defines the calibration screen background, separately from experiment stimulus backgrounds. Choose a color that contrasts with calibration target elements. The upstream example provides a specific default for its own procedure.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_type` — Calibration target type

**In brief:** Graphic type of the calibration target.

**Details:** Chooses the visual style or shape of the calibration target, subject to ioHub driver support. The upstream Tobii configuration includes `CIRCLE_TARGET`. Do not assume arbitrary target types will work without checking the driver.

**Available options:**

- `CIRCLE_TARGET` — Draw the documented two-circle calibration target, controlled by outer/inner diameter and color attributes. No other target types are documented in these files.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.color_type` — Calibration color type

**In brief:** Controls how calibration target color values are interpreted.

**Details:** Identifies how the calibration renderer interprets target color values, for example `rgb` in the supplied configuration. This is distinct from stimulus button and text colors. Values must follow PsychoPy or driver color conventions.

**Available options:**

- `rgb` — Interpret calibration target colors in the documented RGB color mode; this is the supplied mode, not a tested enumeration of alternatives.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.unit_type` — Calibration units

**In brief:** Coordinate and size units used for calibration elements.

**Details:** Selects the coordinate and size units used by the calibration target renderer, such as `pix` in the example. Other unit systems require consistent conversion of diameters and movement values. Verify the on-screen result before recording.

**Available options:**

- `pix` — Interpret target geometry in pixel units as configured in the supplied YAML; other PsychoPy unit modes are not established as supported here.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.outer_diameter` — Target outer diameter

**In brief:** Diameter of the calibration target's outer circle.

**Details:** Sets the diameter of the outer calibration ring in the currently selected target units. It must be considered together with the inner target diameter to keep the marker recognizable. With `pix` these dimensions are specified in pixels.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.outer_stroke_width` — Target outer stroke width

**In brief:** Stroke width of the outer calibration ring.

**Details:** Controls the drawn outline thickness of the outer target circle. Visibility depends on the ring size, line color, and screen contrast. The value is not related to eye-tracking accuracy thresholds.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.outer_fill_color` — Target outer fill color

**In brief:** Fill color of the outer calibration ring.

**Details:** Determines the fill color of the outer calibration circle. The outline uses a separate setting. Choose sufficient contrast against the calibration background and inner circle.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.outer_line_color` — Target outer outline color

**In brief:** Outline color of the outer calibration ring.

**Details:** Defines the color of the outer ring border, in conjunction with its stroke width. It affects only the visual calibration marker. It does not modify the gaze stream or sampling rate.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.inner_diameter` — Target inner diameter

**In brief:** Diameter of the smaller central calibration point.

**Details:** Sets the diameter of the smaller central circle layered over the outer calibration target. It is usually smaller than the outer diameter. The contrast and relative sizes help the participant fixate on the center.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.inner_stroke_width` — Target inner stroke width

**In brief:** Stroke width of the inner calibration point.

**Details:** Controls the line thickness around the inner calibration target. Its visual result depends on target units and circle size. It does not change device calibration mathematics on its own.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.inner_fill_color` — Target inner fill color

**In brief:** Fill color of the inner calibration point.

**Details:** Sets the fill color of the central calibration marker. Use contrast relative to the outer ring so the center remains visible. It is a presentation setting rather than an eye-tracker data field.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.inner_line_color` — Target inner outline color

**In brief:** Outline color of the inner calibration circle.

**Details:** Controls the outline color of the inner circle, used with `inner_stroke_width`. The effect is limited to the calibration target appearance. It does not change raw or filtered gaze values.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.animate.enable` — Animate calibration target

**In brief:** Enables animated motion of the calibration target.

**Details:** Enables driver-supported animation when calibration targets move or change size. When disabled, the target may change positions without animation. Additional animation parameters matter only where this capability is supported.

**Available options:**

- `True` — Animate transitions and target scaling according to the movement and expansion settings.
- `False` — Disable calibration target animation; targets can jump between positions.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.animate.movement_velocity` — Target movement velocity

**In brief:** Movement velocity of the target in pixels per second.

**Details:** Defines the motion speed of a calibration marker transitioning to another position. Excessive speed can make tracking the target visually difficult. It is meaningful only with target animation enabled.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.animate.expansion_ratio` — Target expansion ratio

**In brief:** Maximum expansion ratio of the target's outer circle.

**Details:** Represents the maximum scale of the animated outer target relative to its normal size. A factor of `1.0` means no enlargement. The rendered effect depends on the animation implementation.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.animate.expansion_speed` — Target expansion speed

**In brief:** Speed of target resizing in pixels per second.

**Details:** Controls the pace of expansion during an animated calibration target sequence. This is a visual animation property and must not be confused with sample collection frequency. It is used only if animation is active.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.animate.contract_only` — Contract-only animation

**In brief:** Restricts the size animation to target contraction.

**Details:** When enabled, the animation is limited to shrinking the target from a larger state toward its normal size. When disabled, the target may expand and contract. The behavior requires driver support and enabled target animation.

**Available options:**

- `True` — Start with an expanded outer target and contract it toward its original size.
- `False` — Expand from original size and then contract again.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.runtime_settings.sampling_rate` — Sampling rate

**In brief:** Requested tracker sample rate in Hz, subject to device support.

**Details:** The upstream MouseGaze example documents 50 or 100 Hz, while the sample Tobii configuration uses 60 Hz. This is an ioHub device request, not a monitor refresh-rate control. Physical trackers support model-specific rates, and the GUI neither negotiates nor validates them against hardware.

**Available options:**

- `MouseGaze: 50 Hz` — Emulator generates at 50 samples per second; this is the supplied MouseGaze default.
- `MouseGaze: 100 Hz` — Second documented MouseGaze sampling-rate option; increases event frequency.
- `Tobii: device-supported rate` — Physical Tobii supported sampling rates vary by model; the supplied example sets 60 Hz, but this is not a universal fixed choice.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.runtime_settings.track_eyes` — Tracked eyes

**In brief:** Selects which eye contributes gaze samples.

**Details:** MouseGaze examples report monocular samples with `RIGHT_EYE`, while the shown Tobii configuration uses `BINOCULAR`. Supported settings depend on the specific driver and device. Changing to an unsupported mode may prevent expected data from appearing.

**Available options:**

- `RIGHT_EYE` — Monocular right-eye events emitted by the MouseGaze emulator; this is its documented tracking mode.
- `BINOCULAR` — Binocular events for the supplied Tobii driver configuration; not a MouseGaze mode.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.controls.move` — Gaze movement mouse control

**In brief:** MouseGaze button triggering simulated gaze samples in upstream ioHub.

**Details:** The upstream ioHub MouseGaze configuration uses `controls.move: RIGHT_BUTTON` to trigger simulated gaze sample updates. Keep this distinct from left-clicking experiment answers. This describes upstream behavior; individual demo adapters can implement a different mouse-gating policy.

**Available options:**

- `LEFT_BUTTON` — Generate simulated gaze-position updates using the left mouse button; may conflict with selecting an experiment response.
- `MIDDLE_BUTTON` — Use middle-button presses for simulated gaze-position updates.
- `RIGHT_BUTTON` — Use right-button presses for gaze updates; default in the supplied MouseGaze YAML.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.controls.blink` — Blink mouse control

**In brief:** MouseGaze mouse-button combination for a simulated blink event.

**Details:** The source MouseGaze config combines left and right mouse buttons to emulate a blink event. Holding the gaze-generation button while responding can therefore create conflicting gestures. This does not configure blink detection for physical Tobii devices.

**Available options:**

- `LEFT_BUTTON` — Allow the left mouse button to generate blink events when present in the configured list.
- `MIDDLE_BUTTON` — Allow the middle mouse button to generate blink events when present in the configured list.
- `RIGHT_BUTTON` — Allow the right mouse button to generate blink events when present in the configured list.
- `[LEFT_BUTTON, RIGHT_BUTTON]` — Both listed buttons may generate simulated blink events; this is the example configuration. The field is a YAML list, not a single-value selector.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.controls.saccade_threshold` — Saccade threshold

**In brief:** Saccade detection threshold in degrees of visual angle.

**Details:** This setting belongs to the MouseGaze simulator and is used when generating synthetic saccade events. It is not an answer-click threshold or a Tobii raw-data filter. Interpretation is tied to the configured visual-angle geometry.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.tobii.enable` — Enable Tobii driver

**In brief:** Controls whether ioHub loads the physical Tobii driver.

**Details:** This flag enables the Tobii device entry in the supplied ioHub configuration. A compatible connected eye tracker and functioning driver are still required. Enabling the setting alone does not prove connection, discovery, or calibration.

**Available options:**

- `True` — Load the Tobii ioHub driver from this file when the overall runtime also enables tracking.
- `False` — Do not enable the Tobii device configuration; a physical Tobii tracker will not be initialized through this block.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/eyetracker_config.yaml

### `iohub.tobii.model_name` — Tobii model name

**In brief:** Optional filter for a specific eye-tracker model.

**Details:** Optionally filter discovered Tobii trackers by a specified model name. With a single compatible device the field can often remain empty, depending on driver expectations. An incorrect filter can make an available device appear absent.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/eyetracker_config.yaml

### `iohub.tobii.serial_number` — Tobii serial number

**In brief:** Optional serial-number filter for selecting a physical Tobii tracker.

**Details:** A serial number can disambiguate multiple compatible trackers. An empty value does not force a particular serial number, whereas an incorrect one may prevent selection. The GUI neither discovers devices nor validates their serial numbers.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/eyetracker_config.yaml

### `iohub.tobii.manufacturer_name` — Tobii manufacturer name

**In brief:** Manufacturer name recorded in the ioHub configuration.

**Details:** The source YAML uses `Tobii Technology` as informational manufacturer metadata. It does not configure calibration type or select a particular tracker by itself. Use model and serial filters where hardware-specific selection is needed.

**Availability:** `iohub-only` — ioHub configuration; GUI only selects the file path

**Source:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/eyetracker_config.yaml
