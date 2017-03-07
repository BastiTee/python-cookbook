r"""This module contains command line call tools."""
import platform
import subprocess
import os
import logging

def execute_command (command, suppress_stdout=False, suppress_stderr=False,
                useshell=True, workdir=None):
    """Run a command on the command line"""

    log_stdout = []
    handle = subprocess.Popen(command, shell=useshell, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, cwd=workdir)

    while handle.poll() is None:
        line = handle.stdout.readline().strip()
        if not line == None:
            log_stdout.append(line)
            if suppress_stdout == False:
                print (line)

    log_stderr = log_stdout
    handle.stdout.close()
    return handle.returncode, log_stdout, log_stderr

def get_command_process(command, cwd=None, stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE):
    """Creates a subprocess"""

    logging.debug('Invoking: {}'.format(command))
    shell = False
    if get_platform() == 'linux':
        shell = True
    with open(os.devnull, 'w') as fp:
        if not stdin:
            stdin = fp
        if not stdout:
            stdout = fp
        return subprocess.Popen(command, stdin=stdin, stdout=stdout,
                    stderr=stdout, cwd=cwd, shell=shell)

def check_for_command(name, opts=[]):
    """Tests whether an executable with the given name exists on the path"""

    try:
        devnull = open(os.devnull)
        cmdline = [name] + opts
        subprocess.Popen(cmdline, stdout=devnull, stderr=devnull).communicate()
        devnull.close()
    except OSError as e:
        print (e)
        if e.errno == os.errno.ENOENT:
            return False
    return True

def get_platform():
    """Returns the system's platform string"""

    return str(platform.system()).lower()
