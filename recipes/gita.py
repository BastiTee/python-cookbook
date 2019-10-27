#!/usr/bin/env python3
# ==============================================================================
# gita.py
# Run a git command concurrently on any repo in or below the current folder.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# ==============================================================================

from __future__ import with_statement

import os
import re
import sys
from threading import Thread, Lock
try:
    from queue import Queue as queue
except ImportError:  # python 2.x fallback
    from Queue import Queue as queue
import subprocess

MAX_THREADS = 10
MAX_SUBLEVEL = 3  # 0 = only current folder
LOCK = Lock()


class Worker(Thread):

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            self.tasks.task_done()


class ThreadPool:

    def __init__(self, num_threads):
        self.tasks = queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()


def run_git(git_dir, arglist):

    git_dir_title = os.path.basename(git_dir)
    try:
        output = subprocess.check_output(
            arglist, cwd=git_dir, stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as grepexc:
        output = grepexc.output.decode('utf-8')

    output = re.sub('[\n]+', '\n', output)
    output = re.sub('nothing to commit, working directory clean', '', output)
    output = re.sub('^\n', '', output)
    output = re.sub('\n$', '', output)
    global LOCK
    with LOCK:
        if ('up-to-date' in output.lower()
                and not 'untracked files' in output.lower()
                and not 'changes not staged' in output.lower()):
            print(
                '\x1b[0;32m{} - OK\x1b[0m'.format(
                    git_dir_title.upper()))
        else:
            print(
                '\x1b[0;31m--- {}\x1b[0m\n{}'.format(
                    git_dir_title.upper(), output))

if len(sys.argv) == 1:
    print('No git argument provided.')
    exit(1)
sys.argv[0] = 'git'
curr_dir = os.path.abspath(os.getcwd())

git_dirs = []
for dirname, _, filenames in os.walk('.'):
    depth = len(dirname.split(os.path.sep)) - 2
    if depth > MAX_SUBLEVEL:
        continue
    for filename in filenames:
        path = os.path.join(dirname, filename)
        match = re.match('.*\.git/HEAD.*', path, re.IGNORECASE)
        if match != None:
            git_dirs.append(
                os.path.abspath(os.path.dirname(os.path.dirname(path))))
            break

if len(git_dirs) == 0:
    print('No git repositories found.')
    exit(1)

pool = ThreadPool(MAX_THREADS)
for git_dir in git_dirs:
    pool.add_task(run_git, git_dir, sys.argv)
pool.wait_completion()