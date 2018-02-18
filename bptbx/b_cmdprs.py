# -*- coding: utf-8 -*-
"""Command-line parsing presets"""

from argparse import ArgumentParser, Namespace
from os import path, chdir
from re import sub
from bptbx.b_iotools import file_exists, mkdirs

# -----------------------------------------------------------------------------
# INITIALIZATION
# -----------------------------------------------------------------------------


def init(info=''):
    """Initialize a basic argument parser."""
    return ArgumentParser(description=info)


def show_help(prs, message=None):
    """Show argument parser help with a user-message and exit with error."""
    if not isinstance(prs, ArgumentParser):
        raise ValueError('Provided prs object is not of type argument parser.')
    if message:
        print(message, '\n')
    prs.print_help()
    exit(1)

# -----------------------------------------------------------------------------
# ADD METHODS
# -----------------------------------------------------------------------------


def add_file_in(prs, arg='-i', help='Input file'):
    """Add an input file option."""
    arg = _validate_setup_input(prs, arg)
    prs.add_argument(arg, metavar='INPUT', help=help)
    return prs


def add_dir_in(prs, arg='-i', label='Input directory'):
    """Add an input directory option."""
    arg = _validate_setup_input(prs, arg)
    prs.add_argument(arg, metavar='INPUT', help=label)
    return prs


def add_file_out(prs, arg='-o', help='Output file'):
    """Add an output file option."""
    arg = _validate_setup_input(prs, arg)
    prs.add_argument(arg, metavar='OUTPUT', help=help)
    return prs


def add_dir_out(prs, arg='-o', help='Output directory'):
    """Add an output directory option."""
    arg = _validate_setup_input(prs, arg)
    prs.add_argument(arg, metavar='OUTPUT', help=help)
    return prs


def add_bool(prs, arg='-b', help='Option'):
    """Add a toggle option."""
    arg = _validate_setup_input(prs, arg)
    prs.add_argument(arg, action='store_true', help=help)
    return prs


def add_verbose(prs):
    """Add verbose option."""
    add_bool(prs, '-v', 'Verbose output')
    return prs


def add_option(prs, arg='-s', help='Value', default=None):
    """Add an input option."""
    arg = _validate_setup_input(prs, arg)
    help = help if not default else '{} (default: {})'.format(
        help, default)
    prs.add_argument(arg, metavar='VALUE', help=help, default=default)
    return prs


def add_max_threads(prs):
    """Add a max threads option."""
    add_option(prs, '-t', help='Number of threads', default=10)
    return prs


def add_mongo_collection(prs):
    """Add Mongo DB collection option."""
    add_option(prs, '-c', help='MongoDB collection name')

# -----------------------------------------------------------------------------
# CHECK OPTIONS
# -----------------------------------------------------------------------------


def check_file_in(prs, args, arg='-i', optional=False):
    """Check the file option for existence and make path absolute."""
    vargs, arg = _validate_parse_input(prs, args, arg)
    if not vargs.get(arg, None) and not optional:
        show_help(prs, '-' + arg + ': No input file set.')
    elif not vargs.get(arg, None):
        return
    if not path.isfile(vargs[arg]):
        show_help(prs, '-' + arg + ': Given input does not point to a file.')
    if not file_exists(vargs[arg]):
        show_help(prs, '-' + arg + ': Input file does not exist.')
    vargs[arg] = path.abspath(vargs[arg])


def check_dir_in(prs, args, arg='-i', optional=False):
    """Check the directory option for existence and make path absolute."""
    vargs, arg = _validate_parse_input(prs, args, arg)
    if not vargs.get(arg, None) and not optional:
        show_help(prs, '-' + arg + ': No input directory set.')
    elif not vargs.get(arg, None):
        return
    elif not vargs.get(arg, None):
        return
    if not path.isdir(vargs[arg]):
        show_help(prs, '-' + arg + ': Given input does not point to a dir.')
    vargs[arg] = path.abspath(vargs[arg])


def check_file_out(prs, args, arg='-o', optional=False, can_exist=False):
    """Check the output file option."""
    vargs, arg = _validate_parse_input(prs, args, arg)
    if not vargs.get(arg, None) and not optional:
        show_help(prs, '-' + arg + ': No output file set.')
    elif not vargs.get(arg, None):
        return
    if path.isdir(vargs[arg]):
        show_help(prs, '-' + arg + ': Given input does not point to a file.')
    if path.isfile(vargs[arg]) and not can_exist:
        show_help(prs, '-' + arg + ': Output file already exists.')
    vargs[arg] = path.abspath(vargs[arg])


def check_dir_out(prs, args, arg='-o', optional=False, can_exist=True,
                  mk_dir=False, ch_dir=False):
    """Check the output directory option and optionally change to it."""
    vargs, arg = _validate_parse_input(prs, args, arg)
    if not vargs.get(arg, None) and not optional:
        show_help(prs, '-' + arg + ': No output dir set.')
    elif not vargs.get(arg, None):
        return
    if path.isfile(vargs[arg]):
        show_help(prs, '-' + arg + ': Given input does not point to a dir.')
    if path.isdir(vargs[arg]) and not can_exist:
        show_help(prs, '-' + arg + ': Output file already exists.')
    vargs[arg] = path.abspath(vargs[arg])
    if mk_dir:
        mkdirs(vargs[arg])
    if ch_dir:
        chdir(vargs[arg])


def check_option(prs, args, arg='-s', optional=False, is_int=False):
    """Check the input option"""
    vargs, arg = _validate_parse_input(prs, args, arg)
    if not vargs.get(arg, None) and not optional:
        show_help(prs, '-' + arg + ': Not defined.')
    elif not vargs.get(arg, None):
        return
    if is_int:
        try:
            vargs[arg] = int(vargs[arg])
        except ValueError:
            show_help(prs, '-' + arg + ': Requires a number.')


def check_max_threads(prs, args):
    """Check the max threads option."""
    check_option(prs, args, 't', is_int=True)


def check_mongo_collection(prs, args, optional=True):
    """Check Mongo DB collection option."""
    check_option(prs, args, '-c', optional)


# -----------------------------------------------------------------------------
# HELPER METHODS
# -----------------------------------------------------------------------------


def _validate_setup_input(prs, arg):
    if not isinstance(prs, ArgumentParser):
        raise ValueError('Provided prs object is not of type argument parser.')
    if not arg.startswith('-'):
        arg = '-{}'.format(arg)
    return arg


def _validate_parse_input(prs, args, arg):
    if not isinstance(prs, ArgumentParser):
        raise ValueError('Provided prs object is not of type argument parser.')
    if not isinstance(args, Namespace):
        raise ValueError('Provided args object is not of type list.')
    arg = sub('^-+', '', arg)
    return vars(args), arg


# -----------------------------------------------------------------------------
# MAIN / EXAMPLE
# -----------------------------------------------------------------------------


if __name__ == '__main__':
    prs = init('Test')
    # ---
    add_file_in(prs)
    add_file_in(prs, '-j')
    add_file_in(prs, '-k', 'Another input file')
    add_dir_in(prs, '-l')
    add_dir_out(prs)
    add_dir_out(prs, 'p')
    add_bool(prs)
    add_verbose(prs)
    add_option(prs)
    add_option(prs, 'u')
    add_max_threads(prs)
    add_mongo_collection(prs)
    # ---
    prs.print_help()
    args = prs.parse_args()
    # ---
    check_file_in(prs, args)
    check_file_in(prs, args, '-j')
    check_file_in(prs, args, '-k', optional=True)
    check_dir_in(prs, args, 'l')
    check_dir_out(prs, args)
    check_dir_out(prs, args, 'p', optional=True)
    check_option(prs, args)
    check_option(prs, args, 'u', is_int=True)
    check_max_threads(prs, args)
    check_mongo_collection(prs, args, False)
    # ---
    print(args)
