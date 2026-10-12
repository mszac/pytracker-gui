"""UI form contract for fields actually present in supplied native demo YAML."""
from dataclasses import dataclass
from .yamlconfig import get_value


@dataclass(frozen=True)
class Field:
    path: str
    title: str
    kind: str = 'text'
    options: tuple[str, ...] = ()


DATASET_FIELDS = (
    Field('dataset.image.path', 'Katalog obrazów', 'path'),
    Field('dataset.image.bbox_model', 'Model bbox', 'choice', ('grid','superpixel','saliency')),
    Field('dataset.text.path', 'Plik danych CSV', 'path'),
    Field('dataset.text.label_column_name', 'Kolumna etykiet'),
    Field('dataset.text.text_column_name', 'Kolumna tekstu'),
    Field('dataset.text.bbox_model', 'Model bbox', 'choice', ('word','line','sentence')),
    Field('dataset.text.font_height', 'Wysokość fontu', 'int'),
    Field('dataset.text.wrap_fraction', 'Zawijanie tekstu (0–1)', 'float'),
    Field('dataset.time_series.path', 'Plik danych CSV', 'path'),
    Field('dataset.time_series.label_column_name', 'Kolumna klas'),
    Field('dataset.time_series.bbox_model', 'Model bbox', 'choice', ('sample','window')),
    Field('output.folder', 'Katalog wyników', 'path'),
)
MONITOR_FIELDS = (
    Field('display.monitor.name', 'Nazwa monitora'),
    Field('display.monitor.resolution', 'Rozdzielczość (X, Y)', 'pair_int'),
    Field('display.monitor.width', 'Szerokość fizyczna (cm)', 'float'),
    Field('display.monitor.distance', 'Odległość od ekranu (cm)', 'float'),
    Field('display.monitor.display_number', 'Numer ekranu (od 0)', 'int'),
)
APPEARANCE_FIELDS = (
    Field('display.gui.button.size', 'Rozmiar przycisku (X, Y)', 'pair_int'),
    Field('display.gui.button.margin', 'Margines przycisków', 'int'),
    Field('display.gui.button.color', 'Kolor przycisków'),
    Field('display.gui.button.text.color', 'Kolor tekstu przycisków'),
    Field('display.gui.button.text.size', 'Rozmiar tekstu', 'int'),
    Field('display.gui.fixation_dot.size', 'Rozmiar fixation dot', 'int'),
    Field('display.gui.fixation_dot.color', 'Kolor fixation dot'),
    Field('display.gui.aoe', 'Obszar AOE (X, Y)', 'pair_int'),
)


def active_fields(doc, group):
    return tuple(f for f in group if get_value(doc, f.path) is not None)


def to_text(value):
    if isinstance(value, (list, tuple)):
        return ', '.join(map(str, value))
    return '' if value is None else str(value)


def parse_field(field: Field, s: str):
    s = s.strip()
    if field.kind == 'int':
        if not s or ('.' in s): raise ValueError(f'{field.title}: wymagana liczba całkowita')
        return int(s)
    if field.kind == 'float':
        return float(s)
    if field.kind == 'pair_int':
        vals = [p.strip() for p in s.split(',')]
        if len(vals) != 2:
            raise ValueError(f'{field.title}: podaj dwie liczby oddzielone przecinkiem')
        return [int(v) for v in vals]
    if field.kind == 'choice' and s not in field.options:
        raise ValueError(f'{field.title}: dozwolone: {", ".join(field.options)}')
    return s
