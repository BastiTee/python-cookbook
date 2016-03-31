r"""This module contains an extendable daemon implementation."""

import logging
from threading import Lock, Thread
from time import sleep

class Daemon:
    interval = 30.0
    stopped = False
    lock = Lock()
    daemon_locked = False
    
    def __init__(self, interval):
        self.interval = float(interval)

    def start(self):
        while not self.stopped:
            thr = Thread(target=self._invoke_process)
            thr.start()
            sleep(self.interval)
                    
    def stop(self):
        """Not yet implemented."""
        pass

    def _invoke_process(self):
        if self.daemon_locked:
            logging.debug('Daemon already processing')
            return
        self._lock_daemon()
        self._run_daemon_process()
        self._unlock_daemon()
    
    def _run_daemon_process(self):
        """This is the method you need to override in your implementation."""
        pass
    
    def _lock_daemon(self):
        self.lock.acquire()
        self.daemon_locked = True
        self.lock.release()
    
    def _unlock_daemon(self):
        self.lock.acquire()
        self.daemon_locked = False
        self.lock.release()
