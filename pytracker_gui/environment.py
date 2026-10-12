"""Read-only dependency probe using the chosen interpreter; never imports heavy libs in GUI."""
import json
import subprocess
from pathlib import Path


PROBE = r'''
import sys, importlib.util, json
m = {}
for name in ('psychopy', 'tobii_pytracker', 'tobii_research', 'ruamel'):
    try:
        spec = importlib.util.find_spec(name)
        m[name] = None if spec is None else str(spec.origin)
    except Exception as exc:
        m[name] = 'probe-error:' + repr(exc)
print(json.dumps({'executable':sys.executable, 'version':list(sys.version_info[:3]), 'modules':m}))
'''


def probe_interpreter(executable: str):
    if not executable.strip():
        return {'error':'Nie wskazano interpretera Python dla eksperymentów'}
    try:
        result = subprocess.run([executable, '-c', PROBE], capture_output=True,
                                text=True, timeout=8, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'error':str(exc)}
    if result.returncode != 0:
        return {'error':f'Kod {result.returncode}: {result.stderr[:500]}'}
    try: return json.loads(result.stdout)
    except json.JSONDecodeError: return {'error':'Nieczytelna odpowiedź Pythona: ' + result.stdout[:300]}
