# -*- coding: utf-8 -*-
"""Command-line parsing presets"""

from argparse import ArgumentParser, Namespace
from os import path, chdir
from re import sub
from bptbx.b_iotools import file_exists, mkdirs

# -----------------------------------------------------------------------------
# INITIALIZATION
# -----------------------------------------------------------------------------


class ExtendedArgumentParser(ArgumentParser):

    validators = []

    def add_validator(self, func, **kwargs):
        self.validators.append((func, kwargs))

    def parse_and_validate_args(self):
        args = self.parse_args()
        print('args =', args)
        for val in self.validators:
            print('val =', val[0], ' kwargs =', val[1])
            val[0](self, args, **val[1])
        return args


def init(info=''):
    """Initialize an extended argument parser."""
    prs = ExtendedArgumentParser(description=info)
    # prs['test'] = 'yo'
    return prs


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


def add_file_in(prs, arg='-i', help='Input file', **kwargs):
    """Add an input file option."""
    arg = _validate_setup_input(prs, arg)
    kwargs['arg'] = arg
    prs.add_validator(check_file_in, **kwargs)
    prs.add_argument(arg, metavar='INPUT', help=help)
    return prs


def add_dir_in(prs, arg='-i', help='Input directory', **kwargs):
    """Add an input directory option."""
    arg = _validate_setup_input(prs, arg)
    kwargs['arg'] = arg
    prs.add_validator(check_dir_in, **kwargs)
    prs.add_argument(arg, metavar='INPUT', help=help)
    return prs


def add_file_out(prs, arg='-o', help='Output file', **kwargs):
    """Add an output file option."""
    arg = _validate_setup_input(prs, arg)
    kwargs['arg'] = arg
    prs.add_validator(check_file_out, **kwargs)
    prs.add_argument(arg, metavar='OUTPUT', help=help)
    return prs


def add_dir_out(prs, arg='-o', help='Output directory', **kwargs):
    """Add an output directory option."""
    arg = _validate_setup_input(prs, arg)
    kwargs['arg'] = arg
    prs.add_validator(check_dir_out, **kwargs)
    prs.add_argument(arg, metavar='OUTPUT', help=help)
    return prs


def add_bool(prs, arg='-b', help='Option'):
    """Add a toggle option."""
    arg = _validate_setup_input(prs, arg)
    # This adder has no validator
    prs.add_argument(arg, action='store_true', help=help)
    return prs


def add_option(prs, arg='-s', help='Value', default=None, **kwargs):
    """Add an input option."""
    arg = _validate_setup_input(prs, arg)
    help = help if not default else '{} (default: {})'.format(
        help, default)
    kwargs['arg'] = arg
    prs.add_validator(check_option, **kwargs)
    prs.add_argument(arg, metavar='VALUE', help=help, default=default)
    return prs


def add_verbose(prs, **kwargs):
    """Add verbose option."""
    add_bool(prs, '-v', 'Verbose output')
    return prs


def add_max_threads(prs, **kwargs):
    """Add a max threads option."""
    add_option(prs, '-t', help='Number of threads', default=10)
    return prs


def add_mongo_collection(prs, **kwargs):
    """Add Mongo DB collection option."""
    add_option(prs, '-c', help='MongoDB collection name')

# -----------------------------------------------------------------------------
# CHECK OPTIONS
# -----------------------------------------------------------------------------


def check_file_in(prs, args, **kwargs):
    """Check the file option for existence and make path absolute."""
    arg = kwargs.get('arg', '-i')
    optional = kwargs.get('optional', False)
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


def check_dir_in(prs, args, **kwargs):
    """Check the directory option for existence and make path absolute."""
    arg = kwargs.get('arg', '-i')
    optional = kwargs.get('optional', False)
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


def check_file_out(prs, args, **kwargs):
    """Check the output file option."""
    arg = kwargs.get('arg', '-o')
    optional = kwargs.get('optional', False)
    can_exist = kwargs.get('can_exist', False)
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


def check_dir_out(prs, args, **kwargs):
    """Check the output directory option and optionally change to it."""
    arg = kwargs.get('arg', '-o')
    optional = kwargs.get('optional', False)
    can_exist = kwargs.get('can_exist', True)
    mk_dir = kwargs.get('mk_dir', False)
    ch_dir = kwargs.get('ch_dir', False)
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


def check_option(prs, args, **kwargs):
    """Check the input option"""
    arg = kwargs.get('arg', '-s')
    optional = kwargs.get('optional', False)
    is_int = kwargs.get('is_int', False)
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
    # python3 -m bptbx.b_cmdprs -i test.py -j test.py -l bptbx/ -a new.txt -o
    # dir/ -bv -s test -u 10  -t 4 -c mongo
    prs = init('Test')
    # ---
    add_file_in(prs)
    add_file_in(prs, arg='-j')
    add_file_in(prs, arg='-k', help='Another input file', optional=True)
    add_dir_in(prs, arg='-l')
    add_file_out(prs, arg='a')
    add_dir_out(prs)
    add_dir_out(prs, arg='p', optional=True)
    add_bool(prs)
    add_verbose(prs)
    add_option(prs)
    add_option(prs, arg='u', is_int=True)
    add_max_threads(prs)
    add_mongo_collection(prs)
    # ---
    args = prs.parse_and_validate_args()
    print('---')
    for key in args._get_kwargs():
        print(key)
