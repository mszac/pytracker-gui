"""App-private storage. No modification of upstream or demo sources."""
import json
import os
import shutil
import tempfile
from pathlib import Path


def data_home() -> Path:
    override = os.environ.get('PYTRACKER_GUI_HOME')
    if override:
        return Path(override).expanduser().resolve()
    if os.name == 'nt':
        base = os.environ.get('LOCALAPPDATA') or str(Path.home() / 'AppData' / 'Local')
        return Path(base) / 'pytracker-gui'
    base = os.environ.get('XDG_CONFIG_HOME') or str(Path.home() / '.config')
    return Path(base) / 'pytracker-gui'


def atomic_write(path: Path, data: bytes, backup=True):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '.', suffix='.tmp', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        if backup and path.is_file():
            shutil.copy2(path, path.with_suffix(path.suffix + '.bak'))
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def load_settings(home: Path) -> dict:
    try:
        data = json.loads((home / 'settings.json').read_text(encoding='utf-8'))
        return data if isinstance(data, dict) else {}
    except (FileNotFoundError, ValueError, OSError):
        return {}


def save_settings(home: Path, settings: dict) -> None:
    atomic_write(home / 'settings.json', (json.dumps(settings, indent=2, ensure_ascii=False) + '\n').encode('utf-8'))
