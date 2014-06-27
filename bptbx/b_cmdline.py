r"""This module contains command line call tools."""

import subprocess
import os

def runcommand (command, suppress_stdout=False, suppress_stderr=False, useshell=True):
    """Run a command on the command line"""
    
    log_stdout = []
    log_stderr = []
    handle = subprocess.Popen(command, shell=useshell, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        
    while handle.poll() is None:
        line = handle.stdout.readline().strip()
        if not line == None:
            log_stdout.append(line)
            if suppress_stdout == False:
                print line
    
    log_stderr = log_stdout
    return handle.returncode, log_stdout, log_stderr

def checkforcommand(name):
    """Tests whether an executable with the given name exists on the path"""
    
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True
