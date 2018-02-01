r"""This module contains command line call tools."""


def exe(command, workdir=None, suppress_stdout=False,
        suppress_stderr=False, useshell=True):
    """Run a command on the command line (short alias)."""
    return execute_command(command, suppress_stdout, suppress_stderr,
                           useshell, workdir)


def available(command):
    """Test whether an executable exists on the path (short alias)."""
    return check_for_command(command)


def available_list(tools=[]):
    """Test whether a list of executables exists on the path (short alias)."""
    missing_tools = []
    for tool in tools:
        if not available(tool):
            missing_tools.append(tool)
    return missing_tools


def get_platform():
    """Return the system's platform string."""
    import platform
    return str(platform.system()).lower()


def execute_command(command, suppress_stdout=False, suppress_stderr=False,
                    useshell=True, workdir=None):
    """Run a command on the command line."""
    import subprocess
    log_stdout = []
    handle = subprocess.Popen(command, shell=useshell, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, cwd=workdir)

    while handle.poll() is None:
        line = handle.stdout.readline().strip()
        if line:
            line = line.decode()
            log_stdout.append(line)
            if not suppress_stdout:
                print(line)
    log_stderr = log_stdout
    handle.stdout.close()
    return handle.returncode, log_stdout, log_stderr


def get_command_process(command, cwd=None, stdin=None, stdout=None):
    """Create a subprocess."""
    import subprocess
    import os
    if not stdin:
        stdin = subprocess.PIPE
    if not stdout:
        stdout = subprocess.PIPE
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
    """Test whether an executable with the given name exists on the path."""
    import subprocess
    import os
    devnull = open(os.devnull)
    try:
        cmdline = [name] + opts
        subprocess.Popen(
            cmdline, stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        # print(e)
        if e.errno == os.errno.ENOENT:
            return False
    finally:
        devnull.close()
    return True
