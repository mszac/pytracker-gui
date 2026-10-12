"""Non-blocking native process supervisor; only this layer owns experiment PIDs."""
from __future__ import annotations

import os
import queue
import signal
import subprocess
import threading
import json
import time
from pathlib import Path
from .runtime import load_plan, session_binding
from .incremental_log import IncrementalExperimentLog


class ExperimentRunner:
    def __init__(self):
        self.events=queue.Queue()
        self._thread=None
        self._stop=threading.Event()
        self._proc=None
        self._guard=threading.Lock()
        self.log_path=None
        self._stop_worker=None
        self._journal=None
        self.log_write_error=None

    @property
    def running(self):
        return self._thread is not None and self._thread.is_alive()

    def start(self, manifest):
        if self.running:
            raise RuntimeError('A demonstration is already running')
        plan=load_plan(manifest)
        self.log_path=None
        self._run_directory=Path(manifest).resolve().parent
        self._stop.clear()
        self.log_write_error=None
        # The only persistent log is written by a low-priority independent worker.
        # Prepare/start it before launching PsychoPy; no permanent per-line I/O
        # happens on the subprocess reader thread.
        self._journal=IncrementalExperimentLog(
            self._run_directory, plan['run_id'],
            self._run_directory.name.rsplit('_', 1)[0])
        self._journal.start()
        self._log('[RUN] '+str(manifest)+'\n')
        self._thread=threading.Thread(target=self._execute,args=(str(manifest),plan),daemon=True)
        self._thread.start()

    def _log(self, line):
        self.events.put(('log', line))
        if self._journal is not None:
            self._journal.append(line)

    def _finish_log(self, final):
        # Do not block experiment completion waiting for the storage device.
        if self._journal is not None:
            interrupted = (final == 'CANCELLED' or final.startswith('FAILED: process error'))
            self._journal.finish(interrupted=interrupted)
            self.log_path = (self._journal.partial_path if interrupted else
                             self._journal.complete_path)

    def _execute(self, manifest, plan):
        final='PROCESS COMPLETE — COLLECTION NOT VERIFIED'
        verified=[]
        try:
            for step in plan['steps']:
                if self._stop.is_set():
                    final='CANCELLED';break
                self._log('[STATUS] RUNNING: '+step['name']+'\n')
                self.events.put(('state','RUNNING: '+step['name']))
                cmd=[plan['python'],'-u','-m','pytracker_gui.launch_child',manifest,step['key']]
                env=os.environ.copy()
                src=str(Path(__file__).resolve().parent.parent)
                env['PYTHONPATH']=src+os.pathsep+env.get('PYTHONPATH','')
                flags={'cwd':plan['demo_root'],'stdout':subprocess.PIPE,'stderr':subprocess.STDOUT,
                       'stdin':subprocess.DEVNULL,'text':True,'errors':'replace','bufsize':1,'env':env}
                if os.name=='nt':
                    flags['creationflags']=subprocess.CREATE_NEW_PROCESS_GROUP
                else:
                    flags['start_new_session']=True
                proc=subprocess.Popen(cmd,**flags)
                with self._guard:
                    self._proc=proc
                self._log('> '+subprocess.list2cmdline(cmd)+'\n')
                validated=False
                for line in proc.stdout:
                    self._log(line)
                    if line.startswith('[COLLECTION] PASS:'):
                        validated=True
                proc.stdout.close()
                rc=proc.wait()
                with self._guard:
                    self._proc=None
                self._log(f'[PROCESS] block={step["key"]} exit={rc}\n')
                if self._stop.is_set():
                    final='CANCELLED';break
                if rc:
                    final=f'FAILED: {step["key"]}, exit {rc}'
                    break
                # A validator message cannot mark a run verified if its
                # run-ID-scoped measurement CSV is missing or ambiguous.
                try:
                    bound = session_binding(step)['state'] == 'linked'
                except OSError as exc:
                    bound = False
                    self._log('[SESSION] Binding inspection failed: ' + str(exc) + '\n')
                if validated and not bound:
                    self._log('[SESSION] Validator PASS rejected: exact CSV binding unavailable\n')
                verified.append(validated and bound)
            if final.startswith('PROCESS COMPLETE') and all(verified) and verified:
                final='PROCESS COMPLETE — COLLECTION VALIDATED'
            try:
                self._save_result(manifest,final)
            except OSError as exc:
                self._log('[LOG] Could not save result: '+str(exc)+'\n')
            self._log('[FINAL] '+final+'\n')
            self._finish_log(final)
            self.events.put(('done',final))
        except Exception as exc:
            self._log('[ERROR] '+repr(exc)+'\n')
            try:
                self._save_result(manifest,'FAILED: process error')
            except OSError as error:
                self._log('[LOG] Could not save result: '+str(error)+'\n')
            self._log('[FINAL] FAILED: process error\n')
            self._finish_log('FAILED: process error')
            self.events.put(('done','FAILED: process error'))

    def _save_result(self, manifest, result):
        from .storage import atomic_write
        target=Path(manifest).resolve().parent/'result.json'
        # Bind every block to one exact measurement CSV, or record explicitly
        # why no unique file can be associated. Only inspect after child exit.
        plan = load_plan(manifest)
        bindings = {}
        for step in plan['steps']:
            try:
                bindings[step['key']] = session_binding(step)
            except OSError as exc:
                bindings[step['key']] = {'block':step['key'], 'state':'unresolved',
                                         'output_root':step['output_folder'], 'reason':str(exc)}
        payload={'status':result, 'run_id':plan['run_id'],
                 'finished_epoch':time.time(), 'measurement_sessions':bindings}
        atomic_write(target,(json.dumps(payload,ensure_ascii=False,indent=2)+'\n').encode('utf-8'),backup=False)

    def _terminate_tree(self, proc):
        if proc.poll() is not None:
            return
        if os.name=='nt':
            try:
                subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],
                               stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=8,check=False)
            except (OSError, subprocess.TimeoutExpired):
                pass
            if proc.poll() is None:
                try: proc.kill()
                except OSError: pass
        else:
            try: os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError: return
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                if proc.poll() is None:
                    try: os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError: pass

    def stop(self, *, wait=False):
        if not self.running:
            return
        self._stop.set()
        with self._guard:
            proc=self._proc
        if proc is not None and proc.poll() is None:
            self._stop_worker=threading.Thread(target=self._terminate_tree,args=(proc,),daemon=True)
            self._stop_worker.start()
        self._log('[STATUS] STOPPING\n')
        self.events.put(('state','STOPPING'))
        if wait:
            if self._stop_worker is not None:
                self._stop_worker.join(timeout=9)
            if self._thread is not None:
                self._thread.join(timeout=4)
