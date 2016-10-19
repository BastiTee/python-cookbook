r"""This module is used to handle interchangable support for python 2 and 3."""

def _get_python_major_version():
    """Returns the integer value of the major version of Python
    that runs this script."""
    import sys
    return int(sys.version_info[0])

def get_config_parser():
    if _get_python_major_version() <= 2:
        import ConfigParser
        return ConfigParser.ConfigParser
    else:
        from configparser import ConfigParser
        return ConfigParser

def get_queue():
    if _get_python_major_version() <= 2:
        from Queue import Queue
        return Queue
    else:
        from queue import Queue
        return Queue

def get_urllib2():
    if _get_python_major_version() <= 2:
        import urllib2
        return urllib2
    else:
        from urllib import request
        return request

def get_tk():
    if _get_python_major_version() <= 2:
        from Tkinter import Tk, tkMessageBox, tkFileDialog
        messagebox = tkMessageBox 
        filedialog = tkFileDialog
    else:
        from tkinter import Tk, messagebox, filedialog
    return Tk, messagebox, filedialog

def iterator_next(iterator):
    if _get_python_major_version() <= 2:
        return iterator.next()
    else:
        return iterator.__next__()