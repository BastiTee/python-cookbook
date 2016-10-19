r"""This module is used to handle interchangable support for python 2 and 3."""

def get_python_major_version():
    """Returns the integer value of the major version of Python
    that runs this script."""

    import sys
    return int(sys.version_info[0])

def b_configparser():
    """Handles the all-lowercase convention for packages in Python 3 for
    package configparser."""

    if get_python_major_version() <= 2:
        import ConfigParser
        return ConfigParser.ConfigParser
    else:
        from configparser import ConfigParser
        return ConfigParser

def b_queue():
    """Handles the all-lowercase convention for packages in Python 3 for
    package queue."""

    if get_python_major_version() <= 2:
        from Queue import Queue
        return Queue
    else:
        from queue import Queue
        return Queue

def b_urllib2():
    """In python 3 urllib2 was merged into urllib.request."""

    if get_python_major_version() <= 2:
        import urllib2
        return urllib2
    else:
        from urllib import request
        return request

def b_tk():
    """Handles the all-lowercase convention for packages in Python 3 for
    package tkinter. Furthermore some modules in Tk were renamed."""

    if get_python_major_version() <= 2:
        import Tkinter, tkMessageBox, tkFileDialog
        tk = Tkinter.Tk
        mb = tkMessageBox
        fd = tkFileDialog
    else:
        from tkinter import Tk, messagebox, filedialog
        tk = Tk
        mb = messagebox
        fd = filedialog
    return tk, mb, fd

def b_raw_input():
    """In python 3 raw_input() was renamed to input()"""

    if get_python_major_version() <= 2:
        return raw_input()
    else:
        return input()

def b_next(iterator):
    """In python 3 the next method for iterators was renamed to __next__"""

    if get_python_major_version() <= 2:
        return iterator.next()
    else:
        return iterator.__next__()

def b_filter(filter_function, input_list):
    """In python 3, filter does not return a list anymore but an iterator."""

    return_value = filter(filter_function, input_list)
    if not get_python_major_version() <= 2:
        return_value = list(return_value)
    return return_value

def _cmp_to_key(_input_cmp):
    """Converts a cmp= function into a key= function"""

    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return _input_cmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return _input_cmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return _input_cmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return _input_cmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return _input_cmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return _input_cmp(self.obj, other.obj) != 0
    return K

def b_sorted(input_list, cmp=None):
    """In python 3 the cmp argument for sorted function was replaced with
    key."""

    if get_python_major_version() <= 2:
        return sorted(input_list, cmp=cmp)
    else:
        cp_key = _cmp_to_key(cmp)
        return sorted(input_list, key=cp_key)
