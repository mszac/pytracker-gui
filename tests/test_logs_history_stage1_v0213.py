"""Read-only Logs dashboard stage 1: isolated project history and snapshots."""
import json
import os
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.log_history import list_projects, list_runs, read_run
from pytracker_gui.logs_screen import LogsHistoryScreen
from pytracker_gui.theme import apply_theme


def build_run(project, folder='20261012_101530_aB9z0', log='complete'):
    run = project / 'experiments' / folder
    run.mkdir(parents=True, exist_ok=True)
    id_ = folder.rsplit('_', 1)[-1]
    ts = folder[:15]
    plan = {'schema': 2, 'run_id': id_, 'started_at': ts, 'project_name': project.name,
            'demo_key': 'ux_pl', 'gaze': 'mouse', 'voice': False, 'raw_data': True,
            'log_level':'info', 'python': 'C:/python/python.exe', 'eye_config': 'x/eyetracker.yaml',
            'steps':[{'key':'main', 'trials':12, 'config':'not_used'}]}
    (run / 'run.json').write_text(json.dumps(plan), encoding='utf8')
    (run / 'gui-settings.json').write_text(json.dumps({'gui':{'language':'pl'}}), encoding='utf8')
    (run / 'main.yaml').write_text('''dataset:
  text:
    path: x/demo.csv
    bbox_model: word
display:
  monitor:
    name: display-1
    resolution: [1920, 1080]
  gui:
    button:
      size: [250, 50]
      text:
        size: 22
output:
  folder: x/output
''', encoding='utf8')
    if log == 'complete':
        (run / ('experiment_' + folder + '.log')).write_text('[FINAL] OK\n')
    elif log == 'partial':
        (run / ('experiment_' + folder + '.log.part')).write_text('[LOG] INTERRUPTED\n')
    (run / 'result.json').write_text(json.dumps({'status':'FAILED: one block, exit 1'}))
    return run


class ModelTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.projects = self.root / 'projects'
        self.projects.mkdir()
        self.a = self.projects / 'Alpha'
        self.a.mkdir()
        (self.a / 'experiments').mkdir()
        self.b = self.projects / 'Beta'
        self.b.mkdir()
        (self.b / 'experiments').mkdir()

    def test_project_discovery_directory_contract_and_empty_group(self):
        (self.projects / 'NoHistory').mkdir()
        self.assertEqual([(p.name,p.run_count) for p in list_projects(self.projects)], [('Alpha',0),('Beta',0)])
        build_run(self.a)
        self.assertEqual([(p.name,p.run_count) for p in list_projects(self.projects)], [('Alpha',1),('Beta',0)])

    def test_newest_first_and_independent_run_ids(self):
        build_run(self.a, log='partial')
        build_run(self.a, '20261013_111530_qR73x', log='complete')
        self.assertEqual([(r.run_id,r.journal) for r in list_runs(self.a)], [('qR73x','complete'),('aB9z0','partial')])
        self.assertEqual(list_runs(self.b), [])

    def test_canonical_status_is_log_integrity_not_experiment_success(self):
        build_run(self.a)
        report = read_run(list_runs(self.a)[0], list_projects(self.projects)[0])
        self.assertEqual(report['journal'], 'complete')
        self.assertIn('FAILED', report['process_status'])
        self.assertEqual(report['gaze'],'mouse')
        self.assertEqual(report['trials'], 'main: 12')
        self.assertEqual(report['resolution'], '1920, 1080')
        self.assertEqual(report['data'], 'demo.csv')
        self.assertEqual(report['button_size'], '250, 50')
        self.assertEqual(len(report['yaml_details']), 1)
        self.assertFalse((self.a/'experiments'/'20261012_101530_aB9z0'/'data.csv').exists())

    def test_unfinished_and_missing_journal_are_distinct(self):
        build_run(self.a, log='partial')
        self.assertEqual(list_runs(self.a)[0].journal,'partial')
        build_run(self.b, log='none')
        self.assertEqual(list_runs(self.b)[0].journal,'none')

    def test_invalid_and_unsafe_history_is_not_traversed(self):
        build_run(self.a)
        (self.a / 'experiments' / 'not_run').mkdir()
        if hasattr(os, 'symlink'):
            try: (self.projects / 'Alias').symlink_to(self.a, target_is_directory=True)
            except (OSError, NotImplementedError): pass
        self.assertNotIn('Alias', [p.name for p in list_projects(self.projects)])
        self.assertEqual(len(list_runs(self.a)),1)
        bad = self.a / 'experiments' / '20261012_101530_aB9z0' / 'run.json'
        obj = json.loads(bad.read_text());obj['run_id']='WRONG';bad.write_text(json.dumps(obj))
        with self.assertRaisesRegex(ValueError,'run ID'):
            read_run(list_runs(self.a)[0],list_projects(self.projects)[0])

    def test_missing_yaml_is_gracefully_described(self):
        run = build_run(self.a)
        (run / 'main.yaml').unlink()
        report = read_run(list_runs(self.a)[0], list_projects(self.projects)[0])
        self.assertEqual(report['yaml_details'], [])
        self.assertIn('main.yaml', report['yaml_errors'])


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name=='nt', 'Tk display required')
class GuiTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.project = self.base/'projects'/'UXProject'
        build_run(self.project, log='partial')
        self.root = tk.Tk()
        self.root.withdraw()
        apply_theme(self.root)
        self.screen = LogsHistoryScreen(self.root,self.base/'projects')
        self.screen.pack(fill='both',expand=True)
        self.root.update()
        self.addCleanup(self.root.destroy)

    def test_project_run_selection_and_reports_are_read_only(self):
        self.assertEqual(self.screen.selected_project.name,'UXProject')
        self.assertEqual(self.screen.selected_run.run_id, 'aB9z0')
        self.assertEqual(self.screen.report['journal'], 'partial')
        self.assertEqual(str(self.screen.console_btn.cget('text')),'Log konsoli')
        self.assertNotIn('disabled',self.screen.console_btn.state())
        with patch('pytracker_gui.logs_screen.read_run', wraps=read_run) as reader:
            self.screen._toggle_details()
            self.assertTrue(self.screen._expanded)
            self.screen._toggle_details()
            self.assertFalse(self.screen._expanded)
            self.assertEqual(reader.call_count, 0)  # cached settings; toggling is disk-free
        self.assertEqual(list(self.project.glob('experiments/*/console_*.log')),[])

    def test_refresh_preserves_selection_and_switch_language(self):
        build_run(self.project,'20261013_101530_qW3e5',log='complete')
        self.screen.refresh()
        self.assertEqual(self.screen.selected_run.run_id,'aB9z0')
        self.screen.run_list.selection_clear(0,'end')
        self.screen.run_list.selection_set(0)
        self.screen._choose_run(None)
        self.assertEqual(self.screen.selected_run.run_id,'qW3e5')
        self.screen.set_language('en')
        self.assertEqual(self.screen.title_label.cget('text'),'Experiment logs')
        self.assertEqual(self.screen.selected_run.run_id,'qW3e5')
        self.assertEqual(self.screen.report['journal'],'complete')


if __name__ == '__main__': unittest.main()
