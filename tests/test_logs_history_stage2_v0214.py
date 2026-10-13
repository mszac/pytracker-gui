"""Stage-2 bounded log viewer, safe run identity, UX locale and palette."""
from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import tkinter as tk

from pytracker_gui.log_viewer import PAGE_BYTES, journal_for_run, read_page, tail_offset
from pytracker_gui.log_history import list_projects, list_runs
from pytracker_gui.logs_screen import LogsHistoryScreen, ACCENTS
from pytracker_gui.theme import apply_theme
from tests.test_logs_history_stage1_v0213 import build_run


class BoundedReaderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.proj = self.root/'projects'/'Alpha'
        self.run = build_run(self.proj, log='complete')
        self.path = next(self.run.glob('*.log'))
        self.record = list_runs(self.proj)[0]

    def test_exact_log_name_rejects_foreign_journals(self):
        self.path.unlink()
        (self.run/'experiment_unrelated.log').write_text('incorrect')
        path, state = journal_for_run(self.record)
        self.assertIsNone(path)
        self.assertEqual(state, 'none')
        self.assertEqual(list_runs(self.proj)[0].journal, 'none')

    def test_partial_wins_if_both_exist(self):
        part = Path(str(self.path)+'.part')
        part.write_text('[LOG] INTERRUPTED')
        path, state = journal_for_run(self.record)
        self.assertEqual((path, state), (part, 'partial'))
        self.assertEqual(list_runs(self.proj)[0].journal, 'partial')

    def test_small_utf8_log_complete_and_no_padding(self):
        raw = 'Żółć 😀\nzażółć\n'
        self.path.write_text(raw, encoding='utf8')
        text, start, end, size = read_page(self.path)
        self.assertEqual((text, start, end, size), (raw, 0, len(raw.encode()), len(raw.encode())))
        self.assertEqual(tail_offset(self.path), 0)

    def test_multiple_64k_pages_no_full_read(self):
        records = ''.join(f'Line {i:05d} Żółć\n' for i in range(18000))
        self.path.write_text(records, encoding='utf8')
        pos = 0
        results=[]
        for _ in range(20):
            text, start, end, total = read_page(self.path,pos)
            self.assertLessEqual(end - start,PAGE_BYTES)
            self.assertGreater(end,start)
            results.append(text)
            pos=end
            if end == total: break
        self.assertEqual(''.join(results),records)
        self.assertGreater(len(results),3)
        tail = tail_offset(self.path)
        self.assertGreater(tail,0)
        text, _, _, _ = read_page(self.path,tail)
        self.assertIn('Line 17999',text)
        self.assertNotIn('Line 00000',text)

    def test_short_line_flood_is_bounded_by_2000_lines(self):
        self.path.write_bytes(b'x\n' * 50000)
        text, start, end, total = read_page(self.path)
        self.assertEqual(start, 0)
        self.assertEqual(text.count('\n'), 2000)
        self.assertEqual(end, 4000)
        self.assertEqual(total, 100000)
        last_start = tail_offset(self.path)
        text, _, _, _ = read_page(self.path, last_start)
        self.assertLessEqual(text.count('\n'), 2000)
        self.assertTrue(text.endswith('\n'))

    def test_growing_partial_is_visible_after_re_read(self):
        self.path.rename(Path(str(self.path)+'.part'))
        part = Path(str(self.path)+'.part')
        self.assertEqual(read_page(part)[0], '[FINAL] OK\n')
        with part.open('a',encoding='utf8') as output: output.write('[LOG] INTERRUPTED\n')
        self.assertIn('INTERRUPTED',read_page(part)[0])

    def test_symlink_rejected_and_invalid_offsets(self):
        link = self.run/'link.log'
        if hasattr(os,'symlink'):
            try:
                link.symlink_to(self.path)
            except (OSError,NotImplementedError):
                pass
            else:
                with self.assertRaises(ValueError): read_page(link)
        with self.assertRaises(ValueError): read_page(self.path,-4)


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name=='nt','Tk display required')
class ScreenTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)
        self.project=self.base/'projects'/'UXProject'
        self.run=build_run(self.project,log='partial')
        self.log=next(self.run.glob('*.log.part'))
        self.root=tk.Tk()
        self.root.geometry('1250x900')
        apply_theme(self.root)
        self.screen=LogsHistoryScreen(self.root,self.base/'projects')
        self.screen.pack(fill='both',expand=True)
        self.root.update()
        self.addCleanup(self.root.destroy)

    def test_font_and_contrast_are_local_only(self):
        self.assertEqual(str(self.screen.run_list.cget('font')).split()[-1],'11')
        self.assertEqual(self.screen.run_list.cget('selectbackground'),ACCENTS['selection'])
        self.assertEqual(self.screen.project_list.cget('selectbackground'),ACCENTS['selection'])
        self.assertNotIn('disabled',self.screen.console_btn.state())

    def test_console_switch_page_copy_and_settings_preservation(self):
        self.log.write_text('test first\n'+('0123456789 line\n'*8000),encoding='utf8')
        self.screen._set_view('console')
        self.root.update()
        self.assertTrue(self.screen._page_end <= PAGE_BYTES)
        self.assertIn('test first',self.screen._page_text)
        self.assertNotIn('disabled',self.screen.console_actions['next'].state())
        self.screen._next_page()
        self.assertGreater(self.screen._page_offset,0)
        self.screen._previous_page()
        self.assertEqual(self.screen._page_offset,0)
        self.screen._latest_page()
        self.assertGreater(self.screen._page_offset,0)
        self.screen._copy_page()
        self.assertEqual(self.root.clipboard_get(),self.screen._page_text)
        self.screen._set_view('settings')
        self.assertEqual(self.screen.report['run_id'],'aB9z0')

    def test_partial_growth_manual_refresh_and_locale(self):
        self.screen._set_view('console')
        self.assertIn('INTERRUPTED',self.screen._page_text)
        with self.log.open('a',encoding='utf8') as f: f.write('newly appended\n')
        self.screen._refresh_console()
        self.assertIn('newly appended',self.screen._page_text)
        self.screen.set_language('en')
        self.assertEqual(self.screen.console_btn.cget('text'),'Console Log')
        self.assertIn('newly appended',self.screen._page_text)

    def test_no_journal_gracefully_visible(self):
        self.log.unlink()
        self.screen.refresh()
        self.screen._set_view('console')
        self.assertIn('Brak dziennika',self.screen._page_text)
        self.assertIn('disabled',self.screen.console_actions['next'].state())

    def test_load_is_deferred_until_console_selected(self):
        with patch('pytracker_gui.logs_screen.read_page',side_effect=AssertionError('Early file read')):
            self.screen._toggle_details()
            self.screen.set_language('en')
            self.screen.refresh()
        with patch('pytracker_gui.logs_screen.read_page', wraps=read_page) as read:
            self.screen._set_view('console')
            self.assertEqual(read.call_count,1)


if __name__=='__main__':unittest.main()
