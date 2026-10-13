"""Render synchronized Polish and English parameter references from packaged JSON.

`render()` and the default invocation preserve the v0.1.2 Polish-only API.
The GUI still opens no manual window or hyperlink.
"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from pytracker_gui.parameter_help import parameter_catalog, english_tooltip_catalog

GROUP_EN = {
    'Środowisko / GUI': 'Environment / GUI',
    'Dataset / output': 'Dataset / output',
    'Monitor': 'Monitor',
    'Wygląd / layout': 'Appearance / layout',
    'Parametry uruchomienia': 'Launch parameters',
    'ioHub / eye-tracker (manual; nieedytowane obecnie)':
        'ioHub / eye tracker (documented only; currently not editable)',
}
STATUS_PL = {
    'gui': 'Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji',
    'yaml-only': 'Tylko YAML; bez dedykowanego pola formularza',
    'iohub-only': 'Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku',
    'reference': 'Referencyjna opcja upstream/CLI; nie zawsze ma oddzielne pole edycji',
    'future': 'Funkcja oryginalnego silnika, odroczona w GUI',
}
STATUS_EN = {
    'gui': 'GUI field or preference; applied on launch where supported by this feature',
    'yaml-only': 'YAML only; no dedicated form field',
    'iohub-only': 'ioHub configuration; GUI only selects the file path',
    'reference': 'Upstream/CLI reference; not necessarily a dedicated editable field',
    'future': 'Upstream functionality deferred in the GUI',
}
SOURCES = ('[upstream](https://github.com/sbobek/tobii-pytracker), '
           '[demo repository](https://github.com/mszac/tobii-pytracker-demo), '
           '[MouseGaze YAML](https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml), '
           '[Tobii YAML](https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/eyetracker_config.yaml)')


def render(language='pl'):
    if language not in ('pl', 'en'):
        raise ValueError('Unsupported manual language: '+str(language))
    originals = parameter_catalog()
    translations = english_tooltip_catalog() if language == 'en' else {}
    sections = {}
    for key, original in originals.items():
        entry = {**original, **translations.get(key, {})}
        sections.setdefault(original['group'], []).append(entry)
    if language == 'pl':
        lines = [
            '# pytracker-gui — podręcznik parametrów (M1)', '',
            '> Aktualizacja: 2026-10-11, v0.1.5. Opisy odnoszą się do znanych kontraktów',
            '> repozytoriów `sbobek/tobii-pytracker` i `mszac/tobii-pytracker-demo`',
            '> (zestaw dem v1.17.0) oraz do możliwości edytora pytracker-gui.',
            '> Nie stanowią dowodu uruchomienia sprzętu ani gwarancji zachowania',
            '> nowszych, nieprzypiętych do commita wersji upstream.', '',
            'Każdy z **87 parametrów** zawiera krótki opis (jedno zdanie dla ikony `i`)',
            'i opis rozszerzony. Identyfikatory YAML i CLI nie są tłumaczone. **Status `gui`',
            'oznacza pole lub preferencję GUI; zastosowanie zależy od opisanej funkcji.',
            '** Zapis profilu i eksport YAML nie uruchamiają PsychoPy — służy do tego',
            'osobny przycisk Uruchom demo.',
            'Parametry `yaml-only`, `iohub-only`, `reference` i `future`',
            'nie muszą mieć własnych edytorów lub pełnej obsługi wykonawczej.', '',
            'Link **man** w podpowiedzi otwiera odpowiedni wpis w karcie Manual → Index.',
            'Dostępne wartości są opisane dla parametrów, które udostępniają wybór opcji.',
            'Angielska wersja: [`PARAMETER_MANUAL_EN.md`](PARAMETER_MANUAL_EN.md).', '',
            '**Źródła:** '+SOURCES+'.', ''
        ]
        summary='**Krótko:** '; detail='**Opis:** '; availability='**Dostępność:** '
        source='**Źródło:** '
        statuses=STATUS_PL
    else:
        lines = [
            '# pytracker-gui — parameter reference (M1)', '',
            '> Updated: 2026-10-11, v0.2.5. English is the baseline for new option-level documentation.',
            '> Descriptions cover the known contracts of',
            '> `sbobek/tobii-pytracker`, `mszac/tobii-pytracker-demo`',
            '> (v1.17.0 demo set), and the pytracker-gui configuration editor.',
            '> This is not evidence of hardware execution or a guarantee about newer',
            '> upstream commits whose identities have not been pinned.', '',
            'All **87 parameters** provide a one-sentence tooltip and an extended',
            'explanation. YAML and CLI identifiers are deliberately not translated.',
            '**The `gui` status means an editor field or stored preference, not that',
            'an experiment has completed or collected data have been validated.**',
            'Saving a profile or exporting YAML does not launch PsychoPy; use Launch project.',
            'The `yaml-only`, `iohub-only`, `reference` and `future` categories',
            'may lack dedicated editors or complete execution support.', '',
            'Where an item offers discrete choices, the **Available options** section documents each supported or documented value and its effect.',
            'The in-app Manual screen uses this English catalogue as its primary content source; the Polish text remains an independent translation.',
            'Polish edition: [`PARAMETER_MANUAL_PL.md`](PARAMETER_MANUAL_PL.md).', '',
            '**Sources:** '+SOURCES+'.', ''
        ]
        summary='**In brief:** '; detail='**Details:** '; availability='**Availability:** '
        source='**Source:** '
        statuses=STATUS_EN
    for group, items in sections.items():
        label = group if language == 'pl' else GROUP_EN[group]
        lines += ['## '+label, '']
        for item in items:
            lines += [f"### `{item['key']}` — {item['title']}", '',
                      summary+item['short'], '',
                      detail+item['long'], '']
            if item.get('options'):
                lines += [('**Dostępne wartości:**' if language == 'pl' else '**Available options:**'), '']
                for choice in item['options']:
                    lines += [f"- `{choice['value']}` — {choice['description']}"]
                lines += ['']
            lines += [availability+f"`{item['status']}` — {statuses[item['status']]}", '',
                      source+item['source'], '']
    return '\n'.join(lines).rstrip()+'\n'


def render_en():
    return render('en')


def targets():
    return {'pl':HERE/'docs/PARAMETER_MANUAL_PL.md',
            'en':HERE/'docs/PARAMETER_MANUAL_EN.md'}


if __name__ == '__main__':
    if '--check' in sys.argv:
        for lang, path in targets().items():
            if not path.exists() or path.read_text(encoding='utf-8') != render(lang):
                raise SystemExit(f'MANUAL_SYNC_FAIL ({lang}): regenerate with tools/render_parameter_manual.py')
        print('BILINGUAL_MANUAL_SYNC_PASS 87/87 PL+EN')
    else:
        for lang, path in targets().items():
            path.write_text(render(lang), encoding='utf-8')
            print(f'Wrote {path} ({len(parameter_catalog())} parameters)')
