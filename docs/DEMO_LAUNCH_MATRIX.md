# Istniejące demo: rejestr M1 / native

Źródło: bezpośredni audyt dostarczonego `tobii-pytracker-demo v1.17.0` (`tools/run-demo.sh`, `examples/*/run_native*.sh`, `examples/*/run_experiment.py`, 9 YAML). `smoke_text` jest niepublicznym testem, NIE ósmym demo.

| Selector | Variant | Modality | Config (względem demo root) | Trial plan | Backend aktualny | Output folder (default) |
| --- | --- | --- | --- | --- | --- | --- |
| test_demo | en | image | examples/test_demo/config.native.yaml | 3 | upstream CLI | output/test_demo |
| ux_ab_demo | en | text | examples/ux_ab_demo/config.native.yaml | 12 | custom run_experiment.py + install_text_demo | output/ux_ab_demo |
| ux_ab_demo | pl | text | examples/ux_ab_demo/config.native_pl.yaml | 12 | custom + unknown-label=NIE WIEM | output/ux_ab_demo_pl |
| timeseries_noise_demo | machine+pv | time_series | config.machine.native.yaml, config.pv.native.yaml | 9 + 9 **kolejno**, dwóch runów osobno | upstream CLI 2x | output/timeseries_noise_demo/machine, /pv |
| text_search_demo | en | text | examples/text_search_demo/config.native.yaml | 12 | custom + install_text_demo | output/text_search_demo |
| text_search_demo | pl | text | examples/text_search_demo/config.native_pl.yaml | 12 | custom + unknown-label=NIE WIEM | output/text_search_demo_pl |
| image_semantic_demo | en | image | examples/image_semantic_demo/config.native.yaml | 12 | custom + install_image_semantic_demo | output/image_semantic_demo |

## Krytyczny problem przy konfigurowalnych parametrach
Własne `run_experiment.py` w ux_ab, text_search i image_semantic importują oryginalne `tobii_pytracker.main`, instalują adaptery i wywołują `main(...)` z na stałe wpisanymi `enable_eyetracker=True`, `enable_voice=False`, `raw_data=False`, `enable_psychopy=True`, `LOGGER=info`. Dostępne CLI ich `run_experiment.py` pozwala ustawiać tylko config, eye config, loop count, unknown-label (text demos). **Wybranie NO_GAZE/Tobii/voice/raw w GUI i dalsze odpalanie tych wrapperów jest funkcjonalnie BŁĘDNE**. Nie twierdzić, że GUI zmienia te parametry bez zmiany ścieżki uruchomienia.

### Preferowany cienki adapter pytracker-gui (nowy, w GUI child process)
1. Dla `test_demo` i obu bloków `timeseries`: `python -m tobii_pytracker.main --config_file ... --eyetracker_config_file ... [flagi] --loop_count ... --log_level ...`, przy `cwd=demo_root`. Parity wymaga porównania do `tobii-pytracker` entrypoint na wybranym SHA.
2. Dla `ux_ab`, `text_search`, `image_semantic`: uruchamiać osobny `python -m pytracker_gui.runtime.demo_bridge` (lub bezpośredni absolutny child bridge script) w tym samym interpreterze Python 3.10, z `cwd=demo_root`; child importuje `tools.demo_runtime_adapters.install_text_demo` / `install_image_semantic_demo` i `tobii_pytracker.main`, następnie przekazuje **cały jawny** zestaw flag do `main(...)`. Nie kopiować renderera/datasetów. Wariant PL zachowuje odpowiedni label, plik YAML i validators.
3. Alternatywę „mała zmiana w demo run_experiment.py dodająca flags” odrzucamy jako gorszą domyślnie, ponieważ dotyka oddzielnej historii dem i wymaga release parity; dopuszczalna tylko po świadomej decyzji.
4. Wszystkie backendy bez shell=True i bez `bash` w Windows. `PATH`, `sys.path` i `cwd` nie mogą importować `src/tobii_pytracker` z demo repo (authority upstream).

## Kolejność uruchamiania i walidacja
- `cwd` = demo root (tam, gdzie `tools/` i `examples/`); ścieżki w YAML domyślnie relatywne do niego, fizyczne źródło YAML może leżeć w app workspace.
- Używać absolutnej ścieżki do interpretera Python 3.10 i dokładnych argv (po quoting dla GUI preview, lecz bez wykonania stringa w shell).
- Before-run: preflight + dataset path/CSV columns, candidate output collision check, YAML snapshot+hash, time T0.
- After-run: real validator `examples/*/validate_collection.py` z odpowiednim min-mtime/started-at, dla timeseries 2 niezależne bloki. Problem: dostarczone walidatory są nastawione na nagrania MouseGaze i mogą nie przejść w NO_GAZE; w tym trybie potrzebny będzie **osobny jawnie oznaczony behavioral-only** walidator, bez fałszywego GAZE_PASS.
- UI statusy: RUN_EXIT, COLLECTION_VALIDATION, GAZE_QC, CANCELLED; `0` exit ≠ valid collection.
- Semantyka stop: zachować child-group lifecycle (Windows console break/cooperative, Linux process group), testować przerwanie pomiędzy blokami timeseries i VoiceRecorder worker.

## Niezmienione zachowania eksperymentu
- Trial pozostaje response-gated; nie dodawać timera odpowiedzi.
- Dema z adapterami zachowują specjalne geometry tekstów i etykietę none oraz mieszane image trials.
- Warianty PL nie są tylko tłumaczeniem GUI: mają własny config/data/output i tekst odpowiedzi.
- Domyślny MouseGaze move: RIGHT pressed, answer LEFT after release. Wybór NO_GAZE pozostawia LEFT answer dostępny.
