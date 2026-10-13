"""Help manual is single-source, exhaustive for seven current demo variants."""
import unittest
from pathlib import Path
from pytracker_gui.fields import DATASET_FIELDS, MONITOR_FIELDS, APPEARANCE_FIELDS
from pytracker_gui.parameter_help import parameter_catalog, get_parameter_help
from pytracker_gui.yamlconfig import load_text
from tools.render_parameter_manual import render

ROOT=Path(__file__).resolve().parents[1]


class HelpManualTests(unittest.TestCase):
    def test_all_exposed_form_fields_and_native_yaml_have_help(self):
        known=parameter_catalog()
        for field in (*DATASET_FIELDS,*MONITOR_FIELDS,*APPEARANCE_FIELDS):
            self.assertIn(field.path,known)
            self.assertEqual(known[field.path]['status'],'gui')
        for path in (ROOT/'tests/fixtures/examples').rglob('*.yaml'):
            doc=load_text(path.read_text(encoding='utf-8'))
            def walk(node,prefix=''):
                if isinstance(node,dict):
                    for key,val in node.items():
                        walk(val, f'{prefix}.{key}' if prefix else key)
                else:
                    self.assertIn(prefix,known,f'Undocumented demo YAML key {prefix} in {path.name}')
            walk(doc)

    def test_doc_is_substantial_and_reports_source_and_scope(self):
        known=parameter_catalog()
        self.assertGreaterEqual(len(known),75)
        for key,rec in known.items():
            self.assertEqual(key,rec['key'])
            self.assertTrue(rec['short'].endswith('.'),key)
            self.assertGreater(len(rec['long'].split('. ')),2,key)
            self.assertTrue(rec['source'].startswith('https://'),key)
            self.assertIn(rec['status'],('gui','yaml-only','iohub-only','reference','future'))
            self.assertNotIn('\n',rec['short'])
            self.assertLessEqual(len(rec['short']),125,key)
        for key in ('gui.demo_root','gui.upstream_root','gui.python','gui.variant','gui.block',
                    'gui.gaze','gui.iohub_yaml','gui.yaml_editor','gui.profile',
                    'runtime.loop_count','runtime.log_level','runtime.enable_voice','runtime.raw_data',
                    'instructions.intro','instructions.outro',
                    'iohub.controls.move','iohub.tobii.serial_number'):
            self.assertIn(key,known)
            self.assertTrue(get_parameter_help(key)['long'])

    def test_markdown_is_deterministically_generated_from_json(self):
        self.assertEqual((ROOT/'docs/PARAMETER_MANUAL_PL.md').read_text(encoding='utf-8'),render())
        self.assertNotIn('manual hyperlink',render().lower())


if __name__=='__main__':unittest.main()
