#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Basti's Python Toolbox main implementation lookup and executor."""

import inspect
import pkgutil
import importlib
import types
import sys
from re import sub
import readline
import bptbx

callables = []  # a list of all main methods directly callable
prefix = bptbx.__name__ + "."


def _now():
    import time as time_
    return int(round(time_.time() * 1000))


def _hl(message):
    return '\x1b[33m{}\x1b[0m'.format(message)


def _load_main_methods(silent=False):
    for importer, modname, ispkg in pkgutil.iter_modules(
            bptbx.__path__, ''):
        if ispkg:
            continue
        if '__main__' in modname:
            continue
        now = _now()
        module = importlib.import_module(prefix + modname)
        if not silent:
            print(_hl('-- {}\t\t({} ms)'.format(
                modname, (_now() - now))))
        for key, value in inspect.getmembers(module):
            if isinstance(value, types.FunctionType) and \
                    key.startswith('_main'):
                call = sub('^b_', '', modname + '.' + key)
                call = sub('_main_', '', call)
                callables.append(call)
                if not silent:
                    print(_hl('   + ' + call))


def _create_callable_commandline(callable, silent=False):
    if not silent:
        print(_hl('-- creating cmd-line for {}'.format(callable)))
    split = callable.split('.')
    module_name = 'b_{}'.format(split[0])
    method_name = '_main_{}'.format(split[1].split(' ')[0])
    if not silent:
        print(_hl('-- calling {}() from module {}\n'.format(
            method_name, module_name)))
    module = importlib.import_module(prefix + module_name)
    sys.argv = sub('[ ]+', ' ', callable).split(' ')
    return module, method_name


def _completer(text, state):
    options = [x for x in callables if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None


if __name__ == '__main__':

    if len(sys.argv) == 1:
        _load_main_methods()
    else:
        _load_main_methods(True)
    readline.set_completer(_completer)
    readline.parse_and_bind("tab: complete")

    if len(sys.argv) > 1:
        direct_callable = sys.argv[1]
        cmdline = sys.argv[1:]
        if direct_callable not in callables:
            print(_hl('!!! Unknown callable: {}'.format(direct_callable)))
        else:
            module, method_name = _create_callable_commandline(
                ' '.join(cmdline), True)
            getattr(module, method_name)()
            exit(0)

    try:
        while 1:
            inp = input(_hl("> "))
            inp = inp.strip()
            if not inp.split(' ')[0] in callables:
                print(
                    _hl('!!! Unknown callable: {}'.format(inp.split(' ')[0])))
            else:
                try:
                    module, method_name = _create_callable_commandline(inp)
                    getattr(module, method_name)()
                except SystemExit:
                    pass
    except KeyboardInterrupt:
        print()
