import json
import os
import tempfile
import unittest
from pathlib import Path
from pytracker_gui.catalog import CATALOG
from pytracker_gui.fields import DATASET_FIELDS, active_fields, parse_field
from pytracker_gui.profiles import ProfileStore
from pytracker_gui.storage import atomic_write
from pytracker_gui.validation import validate_config, resolve_path
from pytracker_gui.yamlconfig import load_text, dump_doc, read_source, update_value, sha256

FIXTURES=Path(__file__).parent/'fixtures'


class TestCatalog(unittest.TestCase):
    def test_seven_variants_eight_configs(self):
        self.assertEqual(len(CATALOG),7)
        self.assertEqual(sum(len(d.blocks) for d in CATALOG),8)
        self.assertEqual({d.modality for d in CATALOG},{'image','text','time_series'})
        keys=[b.config_relpath for d in CATALOG for b in d.blocks]
        self.assertEqual(len(keys),len(set(keys)))
        self.assertEqual([b.key for b in CATALOG[3].blocks],['machine','pv'])
        self.assertEqual([b.trials for b in CATALOG[3].blocks],[9,9])

    def test_fixtures_exact_names(self):
        for d in CATALOG:
            for b in d.blocks:
                self.assertTrue((FIXTURES/b.config_relpath).is_file())


class TestYaml(unittest.TestCase):
    def test_roundtrip_every_native_config(self):
        for d in CATALOG:
            for b in d.blocks:
                path=FIXTURES/b.config_relpath
                original=path.read_bytes()
                doc,h=read_source(path)
                self.assertEqual(h,sha256(original))
                self.assertEqual(load_text(dump_doc(doc)), doc)

    def test_preserves_unknown_sections_and_comments(self):
        source='''# top comment\ndataset:\n  image: # image comment\n    bbox_model: grid\n    path: old\nunknown_key: # unknown comment\n  list: [one, two]\n'''
        doc=load_text(source)
        update_value(doc,'dataset.image.path','folder with spaces')
        rendered=dump_doc(doc)
        self.assertIn('# top comment',rendered)
        self.assertIn('# image comment',rendered)
        self.assertIn('# unknown comment',rendered)
        self.assertIn('folder with spaces',rendered)
        self.assertEqual(load_text(rendered)['unknown_key']['list'],['one','two'])

    def test_invalid_and_duplicate(self):
        for invalid in ('a: [','x: 1\nx: 2\n','- root is list\n'):
            with self.assertRaises(Exception):load_text(invalid)

    def test_form_changes_keep_types(self):
        doc=load_text('dataset:\n  image:\n    path: abc\n    bbox_model: grid\ndisplay:\n  monitor:\n    resolution: [1920, 1080]\n')
        update_value(doc,'display.monitor.resolution',[1280,720])
        self.assertEqual(load_text(dump_doc(doc))['display']['monitor']['resolution'],[1280,720])
        with self.assertRaises(KeyError):update_value(doc,'totally.unknown','x')
        with self.assertRaises(ValueError):parse_field(next(f for f in DATASET_FIELDS if f.path.endswith('bbox_model') and f.path.startswith('dataset.image')), 'not-a-model')


class TestProfiles(unittest.TestCase):
    def test_isolation_and_integrity_and_stale_warning(self):
        with tempfile.TemporaryDirectory() as temp:
            store=ProfileStore(Path(temp))
            base={'main':'a'*64}
            saved=store.save('test_en',{'main':'dataset:\n  image:\n    path: example\n'},base,'none','',{'loop':'3'})
            self.assertTrue((saved/'main.yaml').is_file())
            got,metadata,stale=store.load('test_en',base)
            self.assertFalse(stale)
            self.assertEqual(metadata['gaze'],'none')
            self.assertEqual(metadata['runtime']['loop'],'3')
            self.assertTrue(store.load('test_en',{'main':'b'*64})[2])
            (saved/'main.yaml').write_text('changed',encoding='utf-8')
            with self.assertRaises(ValueError):store.load('test_en',base)

    def test_atomic_backup(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'file.yaml'
            atomic_write(p,b'first')
            atomic_write(p,b'second')
            self.assertEqual(p.read_bytes(),b'second')
            self.assertEqual((Path(temp)/'file.yaml.bak').read_bytes(),b'first')


class TestValidation(unittest.TestCase):
    def test_good_and_bad_csv(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            data=root/'examples/text_search_demo/data'
            data.mkdir(parents=True)
            (data/'text_search.csv').write_text('answer,selected_text\nyes,hello\n',encoding='utf-8')
            doc=load_text((FIXTURES/'examples/text_search_demo/config.native.yaml').read_text(encoding='utf-8'))
            findings=validate_config(doc,root,'text')
            self.assertFalse([f for f in findings if f.level=='BLOCK'], findings)
            (data/'text_search.csv').write_text('answer,wrong\nyes,x\n',encoding='utf-8')
            findings=validate_config(doc,root,'text')
            self.assertTrue(any('selected_text' in f.detail for f in findings if f.level=='BLOCK'))

    def test_missing_image_and_conflicting_dataset(self):
        doc=load_text((FIXTURES/'examples/test_demo/config.native.yaml').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as temp:
            issues=validate_config(doc,Path(temp),'image')
            self.assertTrue(any(f.level=='BLOCK' for f in issues))
            doc['dataset']['text']={'path':'abc'}
            issues=validate_config(doc,Path(temp),'image')
            self.assertTrue(any('dokładnie jedną' in f.detail for f in issues))

    def test_path_resolver(self):
        with tempfile.TemporaryDirectory(prefix='Zażółć gęślą ') as tmp:
            root=Path(tmp)
            self.assertEqual(resolve_path(root,'folder with spaces'),(root/'folder with spaces').resolve())


if __name__=='__main__':unittest.main()
