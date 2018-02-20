# -*- coding: utf-8 -*-
"""Command-line parsing presets"""

from argparse import ArgumentParser, Namespace
from os import path, chdir
from re import sub
from bptbx.b_iotools import file_exists, mkdirs


class TemplateArgumentParser(ArgumentParser):

    validators = []

    def add_validator(self, func, **kwargs):
        self.validators.append((func, kwargs))

    def _parse_args_super(self, args=None):
        return super(TemplateArgumentParser, self).parse_args(args)

    def parse_args(self):
        args = self._parse_args_super()
        [val[0](args, **val[1]) for val in self.validators]
        return args

    def print_help_and_exit(self, message=None):
        """Show argument parser help with a user-message and exit with error"""
        if message:
            print(message, '\n')
        self.print_help()
        exit(1)

    # ----------------------------------------------------------------
    # ADD METHODS
    # ----------------------------------------------------------------

    def add_file_in(self, arg='-i', help='Input file', **kwargs):
        """Add an input file option."""
        arg = self._validate_setup_input(arg)
        kwargs['arg'] = arg
        self.add_validator(self._check_file_in, **kwargs)
        self.add_argument(arg, metavar='INPUT', help=help)
        return self

    def add_dir_in(self, arg='-i', help='Input directory', **kwargs):
        """Add an input directory option."""
        arg = self._validate_setup_input(arg)
        kwargs['arg'] = arg
        self.add_validator(self._check_dir_in, **kwargs)
        self.add_argument(arg, metavar='INPUT', help=help)
        return self

    def add_file_out(self, arg='-o', help='Output file', **kwargs):
        """Add an output file option."""
        arg = self._validate_setup_input(arg)
        kwargs['arg'] = arg
        self.add_validator(self._check_file_out, **kwargs)
        self.add_argument(arg, metavar='OUTPUT', help=help)
        return self

    def add_dir_out(self, arg='-o', help='Output directory', **kwargs):
        """Add an output directory option."""
        arg = self._validate_setup_input(arg)
        kwargs['arg'] = arg
        self.add_validator(self._check_dir_out, **kwargs)
        self.add_argument(arg, metavar='OUTPUT', help=help)
        return self

    def add_bool(self, arg='-b', help='Option', **kwargs):
        """Add a toggle option."""
        arg = self._validate_setup_input(arg)
        # This adder has no validator
        self.add_argument(arg, action='store_true', help=help, **kwargs)
        return self

    def add_option(self, arg='-s', help='Value', default=None, **kwargs):
        """Add an input option."""
        arg = self._validate_setup_input(arg)
        help = help if not default else '{} (default: {})'.format(
            help, default)
        kwargs['arg'] = arg
        self.add_validator(self._check_option, **kwargs)
        self.add_argument(arg, metavar='VALUE', help=help, default=default)
        return self

    def add_verbose(self, **kwargs):
        """Add verbose option."""
        return self.add_bool('-v', 'Verbose output', **kwargs)

    def add_max_threads(self, **kwargs):
        """Add a max threads option."""
        return self.add_option(
            '-t', help='Number of threads', default=10, **kwargs)

    def add_mongo_collection(self, **kwargs):
        """Add Mongo DB collection option."""
        return self.add_option('-c', help='MongoDB collection name', **kwargs)

    # ----------------------------------------------------------------
    # DEFAULT VALIDATORS
    # ----------------------------------------------------------------

    def _check_file_in(self, args, **kwargs):
        """Check the file option for existence and make path absolute."""
        arg = kwargs.get('arg', '-i')
        optional = kwargs.get('optional', False)
        vargs, arg = self._validate_parse_input(args, arg)
        if not vargs.get(arg, None) and not optional:
            self.print_help_and_exit('-' + arg + ': No input file set.')
        elif not vargs.get(arg, None):
            return
        if not path.isfile(vargs[arg]):
            self.print_help_and_exit('-' + arg +
                                     ': Given input does not point to a file.')
        if not file_exists(vargs[arg]):
            self.print_help_and_exit(
                '-' + arg + ': Input file does not exist.')
        vargs[arg] = path.abspath(vargs[arg])

    def _check_dir_in(self, args, **kwargs):
        """Check the directory option for existence and make path absolute."""
        arg = kwargs.get('arg', '-i')
        optional = kwargs.get('optional', False)
        vargs, arg = self._validate_parse_input(args, arg)
        if not vargs.get(arg, None) and not optional:
            self.print_help_and_exit('-' + arg + ': No input directory set.')
        elif not vargs.get(arg, None):
            return
        elif not vargs.get(arg, None):
            return
        if not path.isdir(vargs[arg]):
            self.print_help_and_exit(
                '-' + arg + ': Given input does not point to a dir.')
        vargs[arg] = path.abspath(vargs[arg])

    def _check_file_out(self, args, **kwargs):
        """Check the output file option."""
        arg = kwargs.get('arg', '-o')
        optional = kwargs.get('optional', False)
        can_exist = kwargs.get('can_exist', False)
        vargs, arg = self._validate_parse_input(args, arg)
        if not vargs.get(arg, None) and not optional:
            self.print_help_and_exit('-' + arg + ': No output file set.')
        elif not vargs.get(arg, None):
            return
        if path.isdir(vargs[arg]):
            self.print_help_and_exit('-' + arg +
                                     ': Given input does not point to a file.')
        if path.isfile(vargs[arg]) and not can_exist:
            self.print_help_and_exit(
                '-' + arg + ': Output file already exists.')
        vargs[arg] = path.abspath(vargs[arg])

    def _check_dir_out(self, args, **kwargs):
        """Check the output directory option and optionally change to it."""
        arg = kwargs.get('arg', '-o')
        optional = kwargs.get('optional', False)
        can_exist = kwargs.get('can_exist', True)
        mk_dir = kwargs.get('mk_dir', False)
        ch_dir = kwargs.get('ch_dir', False)
        vargs, arg = self._validate_parse_input(args, arg)
        if not vargs.get(arg, None) and not optional:
            self.print_help_and_exit('-' + arg + ': No output dir set.')
        elif not vargs.get(arg, None):
            return
        if path.isfile(vargs[arg]):
            self.print_help_and_exit(
                '-' + arg + ': Given input does not point to a dir.')
        if path.isdir(vargs[arg]) and not can_exist:
            self.print_help_and_exit(
                '-' + arg + ': Output directory already exists.')
        vargs[arg] = path.abspath(vargs[arg])
        if mk_dir:
            mkdirs(vargs[arg])
        if not path.isdir(vargs[arg]) and ch_dir:
            self.print_help_and_exit(
                '-' + arg + ': Output directory does not exist.')
        if ch_dir:
            chdir(vargs[arg])

    def _check_option(self, args, **kwargs):
        """Check the input option"""
        arg = kwargs.get('arg', '-s')
        optional = kwargs.get('optional', False)
        is_int = kwargs.get('is_int', False)
        is_float = kwargs.get('is_float', False)
        vargs, arg = self._validate_parse_input(args, arg)
        if not vargs.get(arg, None) and not optional:
            self.print_help_and_exit('-' + arg + ': Not defined.')
        elif not vargs.get(arg, None):
            return
        if is_int:
            try:
                vargs[arg] = int(vargs[arg])
            except ValueError:
                self.print_help_and_exit('-' + arg + ': Requires a number.')
        if is_float:
            try:
                vargs[arg] = float(vargs[arg])
            except ValueError:
                self.print_help_and_exit('-' + arg +
                ': Requires a floating-point number.')

    # ----------------------------------------------------------------
    # HELPER METHODS
    # ----------------------------------------------------------------

    def _validate_setup_input(self, arg):
        if not arg.startswith('-'):
            arg = '-{}'.format(arg)
        return arg

    def _validate_parse_input(self, args, arg):
        if not isinstance(args, Namespace):
            raise ValueError('Provided args object is not of type list.')
        arg = sub('^-+', '', arg)
        return vars(args), arg


# ----------------------------------------------------------------
# MAIN / EXAMPLE
# ----------------------------------------------------------------


if __name__ == '__main__':
    # python3 -m bptbx.b_cmdprs -i test.py -j test.py -l bptbx/ -a new.txt -o
    # dir/ -bv -s test -u 10  -t 4 -c mongo
    prs = TemplateArgumentParser('Test')
    # ---
    prs.add_file_in()
    prs.add_file_in(arg='-j')
    prs.add_file_in(arg='-k', help='Another input file', optional=True)
    prs.add_dir_in(arg='-l')
    prs.add_file_out(arg='a')
    prs.add_dir_out()
    prs.add_dir_out(arg='p', optional=True)
    prs.add_bool()
    prs.add_verbose()
    prs.add_option()
    prs.add_option(arg='u', is_int=True)
    prs.add_max_threads()
    prs.add_mongo_collection()
    # ---
    args = prs.parse_and_validate_args()
    for key in args._get_kwargs():
        print(key)
