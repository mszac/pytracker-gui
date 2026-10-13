# ADR-0008 — Eye source is 3-state, not mouse boolean
Status: ARCHITECTURE DECISION proposed for implementation, derived from upstream main.py and ioHub configs.
Decision: NO_GAZE (CLI enable_eyetracker off, still valid ioHub config file), MOUSEGAZE (enable on + mouse yaml), TOBII (enable on + Tobii yaml). Mouse response remains possible in NO_GAZE; MouseGaze RIGHT move hold/LEFT answer distinct. `--raw_data` cannot manufacture samples when gaze is off. Hardware detection is a preflight, not a self-built tracker backend. Test 3×7 truth-table with hardware gate for real Tobii.
