"""Saved profile snapshots + source provenance; profile is not an upstream config."""
import json
from pathlib import Path
from .storage import atomic_write
from .yamlconfig import sha256
from .projects import portable_eye_reference, resolve_eye_reference


class ProfileStore:
    def __init__(self, home: Path, upstream=None):
        self.home = Path(home)
        self.upstream = upstream

    def profile_dir(self, demo_key: str) -> Path:
        if not demo_key.replace('_','').isalnum():
            raise ValueError('Nieprawidłowy klucz demonstracji')
        return self.home / 'profiles' / demo_key

    def save(self, demo_key: str, docs: dict[str, str], source_shas: dict[str, str], gaze: str, eye_config: str, runtime: dict | None = None):
        if set(docs) != set(source_shas):
            raise ValueError('Niezgodność bloków i hashy źródłowych')
        target = self.profile_dir(demo_key)
        # Validate all YAML and metadata before first write.
        from .yamlconfig import load_text
        for content in docs.values():
            load_text(content)
        meta = {
            'schema': 1, 'demo_key': demo_key, 'source_sha256': source_shas,
            'yaml_sha256': {k: sha256(v.encode('utf-8')) for k,v in docs.items()},
            'gaze': gaze, 'eye_config': eye_config, 'runtime': runtime or {},
            'eye_config_reference': portable_eye_reference(eye_config, self.upstream) if self.upstream and eye_config else None,
        }
        for block, content in docs.items():
            if not block.replace('_','').isalnum():
                raise ValueError('Nieprawidłowy blok YAML')
            atomic_write(target / (block + '.yaml'), content.encode('utf-8'))
        atomic_write(target / 'profile.json', (json.dumps(meta,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
        return target

    def load(self, demo_key: str, source_shas: dict[str, str]):
        target = self.profile_dir(demo_key)
        path = target / 'profile.json'
        if not path.is_file(): return None
        meta = json.loads(path.read_text(encoding='utf-8'))
        if meta.get('schema') != 1 or meta.get('demo_key') != demo_key:
            raise ValueError('Profil ma nieznany format')
        docs = {}
        for k in source_shas:
            blob = (target / (k + '.yaml')).read_bytes()
            if sha256(blob) != meta.get('yaml_sha256',{}).get(k):
                raise ValueError('Uszkodzony lub zmieniony plik profilu: ' + k)
            docs[k] = blob.decode('utf-8')
        if meta.get('eye_config_reference') and self.upstream:
            meta['eye_config'] = resolve_eye_reference(meta['eye_config_reference'], self.upstream)
        elif self.upstream and meta.get('eye_config'):
            # v0.1.6 profiles lack the portable reference. Rebase only canonical
            # upstream configs, never arbitrary external ioHub selections.
            old_path = str(meta['eye_config']).replace('\\', '/')
            basename = old_path.rsplit('/', 1)[-1]
            if (basename in ('mouse_eyetracker_config.yaml', 'eyetracker_config.yaml')
                    and old_path.endswith('/configs/' + basename)):
                candidate = Path(self.upstream) / 'configs' / basename
                if candidate.is_file():
                    meta['eye_config'] = str(candidate.resolve())
        return docs, meta, (meta.get('source_sha256') != source_shas)
