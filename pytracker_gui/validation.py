"""Static checks only. Never equates a static PASS with a working experiment."""
import csv
import os
from dataclasses import dataclass
from pathlib import Path
from .yamlconfig import get_value


@dataclass(frozen=True)
class Finding:
    level: str   # OK, WARN, BLOCK
    detail: str


def resolve_path(root: Path, value: str) -> Path:
    p = Path(os.path.expandvars(str(value))).expanduser()
    return p.resolve() if p.is_absolute() else (root / p).resolve()


def validate_config(doc, root: Path, modality: str, check_files=True):
    issues: list[Finding] = []
    def block(s): issues.append(Finding('BLOCK', s))
    def warn(s): issues.append(Finding('WARN', s))
    def ok(s): issues.append(Finding('OK', s))
    datasets = get_value(doc,'dataset')
    if not isinstance(datasets, dict):
        block('Brak mapy dataset'); return issues
    modes = [m for m in ('image','text','time_series') if datasets.get(m) is not None]
    if len(modes) != 1:
        block('Dataset musi zawierać dokładnie jedną aktywną modalność'); return issues
    mode = modes[0]
    if mode != modality:
        block(f'Demo wymaga modalności {modality}, znaleziono {mode}')
    ds = datasets.get(mode)
    if not isinstance(ds,dict):
        block('Niepoprawna sekcja dataset.' + mode); return issues
    source = ds.get('path')
    if not isinstance(source,str) or not source.strip():
        block('Brak dataset.' + mode + '.path')
    elif check_files:
        p=resolve_path(root,source)
        if mode == 'image':
            if not p.is_dir(): block('Brak katalogu obrazów: ' + str(p))
            else:
                imgs = sum(1 for f in p.rglob('*') if f.is_file() and f.suffix.lower() in ('.jpg','.jpeg','.png','.bmp','.webp'))
                if imgs == 0: block('Katalog nie zawiera plików obrazów: ' + str(p))
                else: ok(f'Znaleziono obrazy: {imgs}')
        else:
            if not p.is_file(): block('Brak pliku danych: ' + str(p))
            else:
                try:
                    with p.open('r', encoding='utf-8-sig', newline='') as file:
                        header = next(csv.reader(file), [])
                    required=[ds.get('label_column_name')]
                    if mode=='text': required.append(ds.get('text_column_name'))
                    for col in required:
                        if not col or col not in header: block('Brak kolumny CSV: ' + str(col))
                    if all(x in header for x in required): ok('CSV: nagłówek i wskazane kolumny są poprawne')
                except (OSError,UnicodeError,csv.Error) as err:
                    block('Odczyt CSV: '+str(err))
    mon = get_value(doc,'display.monitor')
    if not isinstance(mon,dict): block('Brak display.monitor')
    else:
        size=mon.get('resolution')
        if not isinstance(size,list) or len(size)!=2 or any(not isinstance(x,int) or isinstance(x,bool) or x<=0 for x in size):
            block('display.monitor.resolution: wymagane dwie dodatnie liczby całkowite')
        for k in ('width','distance'):
            try:
                if isinstance(mon.get(k),bool) or float(mon.get(k))<=0: raise ValueError()
            except (ValueError, TypeError): block('display.monitor.' + k + ': liczba dodatnia')
        index=mon.get('display_number')
        if not isinstance(index,int) or isinstance(index,bool) or index<0: block('display.monitor.display_number: liczba całkowita >= 0')
    button = get_value(doc,'display.gui.button')
    if not isinstance(button,dict): block('Brak display.gui.button')
    else:
        for key in ('size',):
            v=button.get(key)
            if not isinstance(v,list) or len(v)!=2 or any(not isinstance(i,int) or isinstance(i,bool) or i<=0 for i in v):block('display.gui.button.size: dwie dodatnie liczby')
    aoe = get_value(doc,'display.gui.aoe')
    if not isinstance(aoe,list) or len(aoe)!=2 or any(not isinstance(i,int) or isinstance(i,bool) or i<=0 for i in aoe):
        block('display.gui.aoe: dwie dodatnie liczby')
    inst = get_value(doc,'instructions')
    if not isinstance(inst,dict) or any(not isinstance(inst.get(k),list) or not all(isinstance(s,str) for s in inst.get(k,[])) for k in ('intro','outro')):
        block('instructions.intro/outro: wymagane listy tekstów')
    output = get_value(doc,'output.folder')
    if not isinstance(output,str) or not output.strip():block('Brak output.folder')
    elif check_files:
        out=resolve_path(root,output)
        if out.exists() and not out.is_dir():block('Output wskazuje plik: '+str(out))
        else:
            ancestor=out
            while not ancestor.exists() and ancestor.parent!=ancestor:
                ancestor=ancestor.parent
            if not ancestor.is_dir() or not os.access(ancestor, os.W_OK):
                block('Katalog wyników nie ma zapisywalnego katalogu nadrzędnego: '+str(ancestor))
            else: ok('Output: możliwe utworzenie katalogu (nie wykonywano zapisu)')
    if not any(i.level=='BLOCK' for i in issues):ok('Struktura YAML i kontrolowane pola: PASS (statycznie)')
    warn('Nie wykonano walidacji runtime PsychoPy/ioHub ani urządzenia Tobii.')
    return issues


def check_demo_root(root: Path, demo):
    issues=[]
    if not root.is_dir():return [Finding('BLOCK','Katalog repozytorium dem nie istnieje')]
    if not (root/'tools'/'run-demo.sh').exists():
        issues.append(Finding('WARN','Nie znaleziono tools/run-demo.sh; sprawdź katalog repozytorium dem'))
    for block in demo.blocks:
        if not (root / block.config_relpath).is_file():
            issues.append(Finding('BLOCK','Brak YAML '+block.config_relpath))
    return issues
