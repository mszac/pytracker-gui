"""v0.2.12 single low-priority append-only log and bounded overload recovery."""
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from pytracker_gui.incremental_log import (
    IncrementalExperimentLog, PENDING_BYTES, WRITE_BATCH, WRITE_INTERVAL,
)


class IncrementalLogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run_dir = Path(self.tmp.name)

    def test_single_log_finished_and_stamped(self):
        journal = IncrementalExperimentLog(self.run_dir, 'Ab3xZ', '20261012_013000', interval=.05)
        journal.start()
        for msg in ('[RUN] manifest\n','[STATUS] RUNNING\n','process output\n',
                    '[PROCESS] exit=0\n','[FINAL] COMPLETED\n'):
            journal.append(msg)
        journal.finish()
        self.assertEqual(journal.wait(4), journal.complete_path)
        self.assertEqual(journal.complete_path.read_text(),
                         '[RUN] manifest\n[STATUS] RUNNING\nprocess output\n'
                         '[PROCESS] exit=0\n[FINAL] COMPLETED\n')
        self.assertFalse(journal.partial_path.exists())
        self.assertFalse(list(self.run_dir.glob('console_*.log')))

    def test_interrupted_keeps_part_and_marker(self):
        journal = IncrementalExperimentLog(self.run_dir,'Q7aZ2',interval=.05)
        journal.start()
        journal.append('[STATUS] RUNNING\n')
        journal.finish(interrupted=True)
        self.assertEqual(journal.wait(4), journal.partial_path)
        self.assertIn('[LOG] INTERRUPTED',journal.partial_path.read_text())
        self.assertFalse(journal.complete_path.exists())

    def test_old_pending_data_overwritten_with_explicit_gap_marker(self):
        journal = IncrementalExperimentLog(self.run_dir,'AaB01',interval=.05)
        # Accumulate while writer is unavailable: never grow beyond old 256 KiB.
        for i in range(12):
            journal.append(f'chunk-{i:02d}:' + (str(i % 10) * 32768) + '\n')
            self.assertLessEqual(journal._pending_bytes, PENDING_BYTES)
        self.assertGreater(journal.dropped_bytes, 0)
        journal.start()
        journal.finish()
        self.assertEqual(journal.wait(4),journal.partial_path)
        contents=journal.partial_path.read_text(encoding='utf8',errors='replace')
        self.assertIn('BUFFER_OVERFLOW',contents)
        self.assertIn('chunk-11:',contents)
        self.assertNotIn('chunk-00:',contents)
        self.assertIn('[LOG] INTERRUPTED: BUFFER_OVERFLOW', contents)
        self.assertFalse(journal.complete_path.exists())

    def test_short_producer_calls_do_not_wait_for_filesystem(self):
        journal = IncrementalExperimentLog(self.run_dir,'fF99a',interval=.05)
        # Explicitly hold producer's writer schedule. Enqueue is lock/byte-ring
        # work only and cannot call Path.open or fsync.
        with patch('pathlib.Path.open', side_effect=OSError('disk busy')):
            begin=time.monotonic()
            for i in range(100):
                journal.append('new message\n')
            elapsed=time.monotonic()-begin
        self.assertLess(elapsed, 0.5)
        self.assertLessEqual(journal._pending_bytes, PENDING_BYTES)

    def test_limits_preserved(self):
        self.assertEqual(PENDING_BYTES, 256*1024)
        self.assertEqual(WRITE_BATCH, 64*1024)
        self.assertEqual(WRITE_INTERVAL, 15)


if __name__ == '__main__':
    unittest.main()
