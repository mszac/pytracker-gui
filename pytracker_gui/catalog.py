"""Explicit, immutable inventory grounded in demo repo v1.17.0.

Seven visible launch variants; the time-series variant has two sequential YAML blocks.
No path in this module is a location on the user's machine.
"""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Block:
    key: str
    name: str
    config_relpath: str
    trials: int


@dataclass(frozen=True)
class Demo:
    key: str
    label: str
    variant: str
    modality: str
    engine: str
    description: str
    blocks: tuple[Block, ...]


CATALOG = (
    Demo('test_en', 'Test Demo', 'EN', 'image', 'upstream CLI', '3 fotografie · klasyfikacja obrazów', (
        Block('main', 'Test Demo', 'examples/test_demo/config.native.yaml', 3),)),
    Demo('ux_en', 'UX A/B Text', 'EN', 'text', 'text adapter', '12 zadań · rozmieszczenie informacji', (
        Block('main', 'UX A/B EN', 'examples/ux_ab_demo/config.native.yaml', 12),)),
    Demo('ux_pl', 'UX A/B Text', 'PL', 'text', 'text adapter', '12 zadań · polska wersja', (
        Block('main', 'UX A/B PL', 'examples/ux_ab_demo/config.native_pl.yaml', 12),)),
    Demo('ts_machine_pv', 'Time-Series Noise', 'MACHINE → PV', 'time_series', 'upstream CLI ×2',
         'Dwa bloki uruchamiane kolejno: machine (9), PV (9)', (
        Block('machine', 'Machine Vibration', 'examples/timeseries_noise_demo/config.machine.native.yaml', 9),
        Block('pv', 'PV Power', 'examples/timeseries_noise_demo/config.pv.native.yaml', 9))),
    Demo('search_en', 'Text Search', 'EN', 'text', 'text adapter', '12 zadań · wyszukiwanie informacji', (
        Block('main', 'Text Search EN', 'examples/text_search_demo/config.native.yaml', 12),)),
    Demo('search_pl', 'Text Search', 'PL', 'text', 'text adapter', '12 zadań · polska wersja', (
        Block('main', 'Text Search PL', 'examples/text_search_demo/config.native_pl.yaml', 12),)),
    Demo('image_en', 'Image Semantic', 'EN', 'image', 'image adapter', '12 obrazów · klasyfikacja semantyczna', (
        Block('main', 'Image Semantic', 'examples/image_semantic_demo/config.native.yaml', 12),)),
)
BY_KEY = {d.key: d for d in CATALOG}
assert len(CATALOG) == len(BY_KEY) == 7


def expected_configs(demo: Demo, demo_root: Path):
    return {b.key: demo_root / b.config_relpath for b in demo.blocks}
