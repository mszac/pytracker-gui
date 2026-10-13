"""Native launch contract tests with fake runtime — never opens PsychoPy or Tobii."""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.catalog import CATALOG, BY_KEY
from pytracker_gui.runtime import prepare_run, load_plan, LaunchError, preflight
from pytracker_gui.runner import ExperimentRunner
from pytracker_gui.yamlconfig import read_source, get_value, update_value, dump_doc, load_text

ROOT=Path(__file__).resolve().parents[1]

def console_log(manifest):
    # Historic helper name retained for callers; only ONE new canonical log exists.
    logs = list(manifest.parent.glob('experiment_*.log'))
    partial = list(manifest.parent.glob('experiment_*.log.part'))
    assert len(logs) + len(partial) == 1, (logs, partial)
    return (logs + partial)[0]



class LauncherTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name)
        self.up=self.base/'tobii-pytracker'
        self.demo_root=self.up/'tobii-pytracker-demo'
        (self.up/'src/tobii_pytracker/configs').mkdir(parents=True)
        (self.up/'src/tobii_pytracker/utils').mkdir(parents=True)
        (self.up/'configs').mkdir()
        (self.demo_root/'tools').mkdir(parents=True)
        (self.up/'pyproject.toml').write_text('[build-system]\n',encoding='utf8')
        (self.up/'configs/mouse_eyetracker_config.yaml').write_text('fake: mouse\n',encoding='utf8')
        (self.up/'configs/eyetracker_config.yaml').write_text('fake: tobii\n',encoding='utf8')
        (self.demo_root/'tools/run-demo.sh').write_text('echo fake\n',encoding='utf8')
        for demo in CATALOG:
            for block in demo.blocks:
                dest=self.demo_root/block.config_relpath
                dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(ROOT/'tests/fixtures'/block.config_relpath,dest)
        self.docs={}
        self.demo=BY_KEY['test_en']
        self._select('test_en')
        # Minimal isolated native fake package: no real experiment or hardware.
        fake=self.up/'src/tobii_pytracker'
        (fake/'__init__.py').write_text('',encoding='utf8')
        (fake/'configs/__init__.py').write_text('',encoding='utf8')
        (fake/'utils/__init__.py').write_text('',encoding='utf8')
        (fake/'configs/custom_config.py').write_text('class CustomConfig:\n def __init__(self, filename): self.config_file=filename\n',encoding='utf8')
        (fake/'utils/custom_logger.py').write_text('class CustomLogger:\n def __init__(self,*a): self.logger=None\n',encoding='utf8')
        (fake/'main.py').write_text('''import os,time
LOGGER=None
adapter=None
def main(**kwargs):
 print('FAKE_MAIN',kwargs['config'].config_file,kwargs['enable_eyetracker'],kwargs['raw_data'],kwargs['enable_voice'],adapter,flush=True)
 if os.environ.get('FAKE_BLOCK_SLEEP')=='1': time.sleep(20)
 if os.environ.get('FAKE_BLOCK_FAIL')=='1' and 'machine.yaml' in kwargs['config'].config_file: raise RuntimeError('simulated first-block failure')
''',encoding='utf8')
        (self.demo_root/'tools/__init__.py').write_text('',encoding='utf8')
        (self.demo_root/'tools/demo_runtime_adapters.py').write_text('''def install_text_demo(main_module, label="I DON'T KNOW"):
 main_module.adapter='text'
def install_image_semantic_demo(main_module):
 main_module.adapter='image'
''',encoding='utf8')

    def _select(self,key):
        self.demo=BY_KEY[key]
        self.docs={}
        for block in self.demo.blocks:
            doc,_=read_source(self.demo_root/block.config_relpath)
            ds=get_value(doc,'dataset')[self.demo.modality]
            if self.demo.modality=='image':
                p=self.base/(key+'_'+block.key+'_images')
                p.mkdir(exist_ok=True)
                (p/'sample.png').write_bytes(b'not a real image: static check only')
            else:
                p=self.base/(key+'_'+block.key+'.csv')
                cols=[ds['label_column_name']]
                if self.demo.modality=='text':cols.append(ds['text_column_name'])
                p.write_text(','.join(cols)+'\n'+','.join('some' for _ in cols)+'\n',encoding='utf8')
            update_value(doc,'dataset.'+self.demo.modality+'.path',str(p))
            update_value(doc,'output.folder',str(self.base/'output'/key/block.key))
            self.docs[block.key]=doc

    def _opts(self,**overrides):
        data=dict(home=self.base/'appprivate',demo_key=self.demo.key,docs=self.docs,
                  loops={b.key:b.trials for b in self.demo.blocks},
                  demo_root=self.demo_root,upstream=self.up,python=sys.executable,
                  gaze='none',eye=self.up/'configs/mouse_eyetracker_config.yaml',voice=False,
                  raw_data=False,log_level='info')
        data.update(overrides)
        return data

    def test_registry_all_seven_variants_snapshot_and_source_immutability(self):
        for d in CATALOG:
            self._select(d.key)
            original={b.key:(self.demo_root/b.config_relpath).read_bytes() for b in d.blocks}
            manifest=prepare_run(**self._opts())
            spec=load_plan(manifest)
            self.assertEqual(spec['demo_key'],d.key)
            self.assertEqual([s['key'] for s in spec['steps']],[b.key for b in d.blocks])
            for block in d.blocks:
                self.assertEqual((self.demo_root/block.config_relpath).read_bytes(),original[block.key])
                snapshot = load_text((manifest.parent/(block.key+'.yaml')).read_text('utf8'))
                self.assertEqual(get_value(snapshot, 'output.folder'),
                                 next(s['output_folder'] for s in spec['steps'] if s['key'] == block.key))
                update_value(snapshot, 'output.folder', get_value(self.docs[block.key], 'output.folder'))
                self.assertEqual(dump_doc(snapshot), dump_doc(self.docs[block.key]))

    def test_rejects_no_gaze_raw_missing_eye_bad_trials_and_corrupted_manifest(self):
        errors=preflight(self.demo.key,self.docs,{'main':3},demo_root=self.demo_root,
                upstream=self.up,python=sys.executable,gaze='none',eye='missing.yaml',
                voice=False,raw_data=True,log_level='info')
        self.assertTrue(any('Raw gaze' in v for v in errors))
        self.assertTrue(any('ioHub' in v for v in errors))
        with self.assertRaises(LaunchError):prepare_run(**self._opts(loops={'main':0}))
        manifest=prepare_run(**self._opts())
        data=json.loads(manifest.read_text('utf8'))
        data['steps'][0]['config']=str(self.up/'configs/eyetracker_config.yaml')
        manifest.write_text(json.dumps(data),encoding='utf8')
        with self.assertRaises(LaunchError):load_plan(manifest)

    def _run_fake(self,**kw):
        manifest=prepare_run(**self._opts(**kw))
        runner=ExperimentRunner()
        with patch.dict(os.environ,{'PYTHONPATH':str(self.up/'src')+os.pathsep+os.environ.get('PYTHONPATH','')}):
            runner.start(manifest)
            runner._thread.join(timeout=12)
            runner._journal.wait(4)
        self.assertFalse(runner.running)
        return manifest,runner

    def test_real_subprocess_no_gaze_applies_exact_snapshot(self):
        self._select('test_en')
        manifest,runner=self._run_fake()
        events=list(runner.events.queue)
        logs=''.join(val for kind,val in events if kind=='log')
        self.assertIn('FAKE_MAIN',logs)
        self.assertIn(' False False False None',logs)
        self.assertIn('[COLLECTION] NOT VERIFIED:',logs)
        self.assertIn('PROCESS COMPLETE — COLLECTION NOT VERIFIED',(manifest.parent/'result.json').read_text('utf8'))
        self.assertIn('FAKE_MAIN',console_log(manifest).read_text('utf8'))

    def test_dynamic_mouse_tobii_and_voice_flags(self):
        self._select('test_en')
        for gaze,config in [('mouse','mouse_eyetracker_config.yaml'),
                            ('tobii','eyetracker_config.yaml')]:
            manifest,runner=self._run_fake(gaze=gaze,eye=self.up/'configs'/config,
                                           raw_data=True,voice=True)
            logs=console_log(manifest).read_text('utf8')
            self.assertIn(' True True True None',logs)
            self.assertIn('[COLLECTION] NOT VERIFIED',logs)

    def test_time_series_two_isolated_sequential_children(self):
        self._select('ts_machine_pv')
        manifest,runner=self._run_fake()
        events=list(runner.events.queue)
        logs=''.join(val for kind,val in events if kind=='log')
        self.assertEqual(logs.count('FAKE_MAIN'),2)
        self.assertIn('block=machine exit=0',logs)
        self.assertIn('block=pv exit=0',logs)

    def test_text_and_image_adapter_mode_dynamic(self):
        for key, expected in [('ux_pl','text'),('search_en','text'),('image_en','image')]:
            self._select(key)
            manifest,runner=self._run_fake()
            logs=console_log(manifest).read_text('utf8')
            self.assertIn(' '+expected+'\n',logs)

    def test_failure_stops_before_pv(self):
        self._select('ts_machine_pv')
        with patch.dict(os.environ,{'FAKE_BLOCK_FAIL':'1'}):
            manifest,runner=self._run_fake()
        result=json.loads((manifest.parent/'result.json').read_text('utf8'))
        self.assertIn('FAILED: machine',result['status'])
        log=console_log(manifest).read_text('utf8')
        self.assertNotIn('block=pv',log)

    @unittest.skipIf(os.name=='nt','POSIX-specific signal and process-group check')
    def test_cancel_prevents_followup_block(self):
        self._select('ts_machine_pv')
        manifest=prepare_run(**self._opts())
        runner=ExperimentRunner()
        with patch.dict(os.environ,{'PYTHONPATH':str(self.up/'src'), 'FAKE_BLOCK_SLEEP':'1'}):
            runner.start(manifest)
            for _ in range(100):
                if runner._proc is not None:
                    break
                time.sleep(.03)
            self.assertIsNotNone(runner._proc)
            runner.stop()
            runner._thread.join(6)
            runner._journal.wait(4)
        self.assertFalse(runner.running)
        result=json.loads((manifest.parent/'result.json').read_text('utf8'))
        self.assertEqual(result['status'],'CANCELLED')
        self.assertNotIn('block=pv', console_log(manifest).read_text('utf8'))


if __name__=='__main__': unittest.main()
