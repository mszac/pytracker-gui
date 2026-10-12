"""Discover three independently owned repositories in the canonical nested layout.

Never changes either Git checkout. Paths are derived from the installed GUI location,
not the shell's current working directory.
"""
from pathlib import Path
import sys

from .catalog import CATALOG

DEMO_DIRECTORY = 'tobii-pytracker-demo'
GUI_DIRECTORY = 'pytracker-gui'


def gui_directory() -> Path:
    return Path(__file__).resolve().parent.parent


def valid_upstream(directory: Path) -> bool:
    root = Path(directory)
    return all((root / item).exists() for item in
               ('configs/mouse_eyetracker_config.yaml', 'pyproject.toml', 'src/tobii_pytracker'))


def valid_demo(directory: Path) -> bool:
    root = Path(directory)
    return (root / 'tools/run-demo.sh').is_file() and (root / 'examples').is_dir()


def canonical_roots(gui_root=None):
    gui = (Path(gui_root) if gui_root is not None else gui_directory()).resolve()
    return gui.parent, gui.parent / DEMO_DIRECTORY


def choose_roots(settings=None, *, gui_root=None):
    """Installed-neighbor roots win; valid external legacy roots are fallback only.

    A stale persisted path must not break a newly installed nested checkout.
    """
    settings = settings or {}
    canonical_upstream, canonical_demo = canonical_roots(gui_root)
    saved_upstream = Path(settings['upstream_root']) if settings.get('upstream_root') else None
    saved_demo = Path(settings['demo_root']) if settings.get('demo_root') else None
    if valid_upstream(canonical_upstream):
        upstream = canonical_upstream
    elif saved_upstream is not None and valid_upstream(saved_upstream):
        upstream = saved_upstream.resolve()
    else:
        upstream = canonical_upstream
    expected_demo = upstream / DEMO_DIRECTORY
    if valid_demo(expected_demo):
        demo = expected_demo
    elif saved_demo is not None and valid_demo(saved_demo) and saved_demo.resolve().parent == upstream.resolve():
        demo = saved_demo.resolve()
    else:
        demo = expected_demo
    return upstream, demo


def default_eye_config(upstream_root, gaze):
    filename = 'eyetracker_config.yaml' if gaze == 'tobii' else 'mouse_eyetracker_config.yaml'
    return Path(upstream_root) / 'configs' / filename


def validate_layout(upstream_root, demo_root, *, require_every_config=True):
    """Return independent, actionable errors; no external libraries or mutation."""
    upstream = Path(upstream_root).expanduser().resolve()
    demo = Path(demo_root).expanduser().resolve()
    errors = []
    if not valid_upstream(upstream):
        errors.append('Nie znaleziono oryginalnego tobii-pytracker (src/, pyproject.toml, configs/mouse_eyetracker_config.yaml): ' + str(upstream))
    expected = upstream / DEMO_DIRECTORY
    if demo != expected:
        errors.append('Repo demonstracji musi być w ' + str(expected) + ' (otrzymano: ' + str(demo) + ')')
    if not valid_demo(demo):
        errors.append('Nie znaleziono repo mszac/tobii-pytracker-demo (tools/run-demo.sh i examples/): ' + str(demo))
    if require_every_config and valid_demo(demo):
        for d in CATALOG:
            for block in d.blocks:
                if not (demo / block.config_relpath).is_file():
                    errors.append('Brak konfiguracji [' + d.key + ']: ' + block.config_relpath)
    return errors


def format_layout_report(gui_root=None, python_executable=None):
    gui = Path(gui_root or gui_directory()).resolve()
    upstream, demo = canonical_roots(gui)
    errors = validate_layout(upstream, demo)
    lines = [
        'pytracker-gui — repozytoria M1 (kontrola struktury, bez uruchamiania PsychoPy)',
        'GUI:      ' + str(gui),
        'Upstream: ' + str(upstream),
        'Dema:     ' + str(demo),
        'Python:   ' + str(python_executable or sys.executable),
        'Warianty: ' + str(len(CATALOG)),
    ]
    lines += (['BLOCK: '+err for err in errors] if errors else ['LAYOUT PASS: upstream, dema i wszystkie 8 plików YAML'])
    lines.append('RUNTIME/HARDWARE: NOT RUN')
    return '\n'.join(lines), not errors
