"""Command-line parsing presets."""


from bptbx.b_iotools import file_exists
from argparse import ArgumentParser
from os import path, chdir


def init(info=''):
    """Init argument parser."""
    return ArgumentParser(description=info)


def show_help(prs, message):
    """Show argument parser help."""
    print(message)
    prs.print_help()
    exit(1)


# FILE IN ---------------------------------------------------------------------


def add_file_in(prs):
    """Add an input file option."""
    prs.add_argument('-i', metavar='INPUT', help='Input file')


def check_file_in(prs, args):
    """Check the input file option."""
    if not args.i:
        show_help(prs, 'No input file set.')
    if not file_exists(args.i):
        show_help(prs, 'Input file does not exist.')
    args.i = path.abspath(args.i)


# DIRECTORY IN ----------------------------------------------------------------


def add_dir_in(prs, label='Input directory'):
    """Add an input directory option."""
    prs.add_argument('-i', metavar='INPUT', help=label)


def check_dir_in(prs, args):
    """Check the input directory option."""
    if not args.i:
        show_help(prs, 'No input directory set.')
    if not path.isdir(args.i):
        show_help(prs, 'Input directory does not exist.')
    args.i = path.abspath(args.i)


# FILE OUT --------------------------------------------------------------------


def add_file_out(prs):
    """Add an output file option."""
    prs.add_argument('-o', metavar='OUTPUT', help='Output file')


def check_file_out(prs, args):
    """Check the output file option."""
    if args.o is None:
        show_help(prs, 'No output file provided.')
    if file_exists(args.o):
        show_help(prs, 'Output file already exists.')
    args.o = path.abspath(args.o)


# DIRECTORY OUT ---------------------------------------------------------------


def add_dir_out(prs):
    """Add an output directory option."""
    prs.add_argument('-o', metavar='OUTPUT', help='Output directory')


def check_dir_out_and_chdir(prs, args):
    """Check the output directory option."""
    if not args.o:
        show_help(prs, 'No output directory set.')
    if not path.isdir(args.o):
        show_help(prs, 'Output directory does not exist.')
    args.o = path.abspath(args.o)
    chdir(args.o)
    # r_util.log('Working directory {}'.format(getcwd()))


# AUXILIARY- ------------------------------------------------------------------


def add_opt_dir_in(prs, opt, label):
    """Add an optional input directory option."""
    prs.add_argument(opt, metavar='IN_DIR', help=label)


def check_opt_dir_in(prs, arg, info='Optional directory does not exist.'):
    """Check the optional input directory option."""
    if arg is None:
        return
    if not path.isdir(arg):
        show_help(prs, info)
    return path.abspath(arg)


def add_opt_file_in(prs, opt, label):
    """Add an optional input file option."""
    prs.add_argument(opt, metavar='IN_FILE', help=label)


def check_opt_file_in(prs, arg, info='Optional file does not exist.'):
    """Check the optional input file option."""
    if arg is None:
        return
    if not path.isfile(arg):
        show_help(prs, info)
    return path.abspath(arg)


def add_option(prs, arg, info='Mandatory text value.'):
    """Add a mandatory input option."""
    prs.add_argument(arg, metavar='VALUE', help=info)


def check_option(prs, arg):
    """Check the input file option."""
    if not arg:
        show_help(prs, 'Mandatory option not set.')


def add_verbose(prs):
    """Add verbose option."""
    prs.add_argument('-v', action='store_true',
                     help='Verbose output', default=False)


def add_mongo_collection(prs):
    """Add Mongo DB collection option."""
    prs.add_argument('-c', default='', help='MongoDB collection name')


def check_mongo_collection(prs, args, required=False):
    """Check Mongo DB collection option."""
    if not args.c and required:
        show_help(prs, 'MongoDB collection required but not set.')
    elif not args.c:
        return
    from robota import r_mongo
    col = r_mongo.get_client_for_collection(args.c, create=False)
    if not col:
        show_help(prs, 'Given MongoDB collection does not exist.')
    return col


def add_bool(prs, opt, label):
    """Add a toggle option."""
    prs.add_argument(opt, action='store_true', help=label, default=False)


def add_max_threads(prs):
    """Add a max threads option."""
    prs.add_argument('-t', metavar='THREADS',
                     help='Number of threads', default=10)


def check_max_threads(prs, args):
    """Check the max threads option."""
    try:
        args.t = int(args.t)
    except ValueError:
        show_help(prs, 'Invalid number of threads.')
    if int(args.t) <= 0:
        show_help(prs, 'Invalid number of threads.')
