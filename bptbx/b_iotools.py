r"""This module contains various tools for recurring I/O operations."""

import datetime
import hashlib
import os
import re
import zipfile

from bptbx import b_legacy


def change_to_scriptdir(file):
    """Change to the folder where the script resides."""
    os.chdir(os.path.dirname(os.path.abspath(file)))


def mkdirs(directory):
    """Create directory structure if it does not exist"""

    if not directory:
        raise TypeError('directory not provided.')

    directory_abs = os.path.abspath(directory)
    if not os.path.exists(directory_abs):
        try:
            os.makedirs(directory_abs)
        except FileExistsError:
            pass  # ignore


def get_immediate_subdirectories(file_path, reverse_order=False,
                                 show_hidden=False):
    """Return the sub-directories of a given file path, but
    only the first level."""

    if not file_path:
        raise TypeError('file_path not provided.')

    directories = []
    for name in os.listdir(file_path):
        if os.path.isdir(os.path.join(file_path, name)):
            if show_hidden or not str(name).startswith('.'):
                directories.append(name)
    directories.sort(key=None, reverse=reverse_order)

    return directories


def get_immediate_subfiles(file_path, pattern=None, ignorecase=False):
    """Return the sub-files of a given file path, but
    only the first level."""

    if not file_path:
        raise TypeError('file_path not provided.')

    files = []
    for name in os.listdir(file_path):
        if os.path.isdir(os.path.join(file_path, name)):
            continue
        if pattern:
            if ignorecase and re.match(pattern, name, re.IGNORECASE):
                files.append(name)
            elif re.match(pattern, name):
                files.append(name)
            continue
        files.append(name)
    files.sort()
    return files


def import_modules_with_check(module_names):
    """Checks if a given set of modules exists. Returns a boolean that
    indicates the import success and a list of failed module names"""

    success = True
    failed_modules = []
    for module_name in module_names:
        try:
            map(__import__, [module_name])
        except ImportError:
            success = False
            failed_modules.append(module_name)
    return success, failed_modules


def import_module_with_check(module):
    """Checks if a given module exists. If yes, imports it. If no,
    throws an exception and exits."""

    module_names = [module]
    success, _ = import_modules_with_check(module_names)
    return success


def appendzeros(directory, directories=False):
    """Appends leading zeros to all files or directories in given
    directory path if theses objects have leading numbers."""

    # list all directory content
    dir_contents = os.listdir(directory)

    # create an array of signed integers
    nos = []
    directories = []

    for dir_content in dir_contents:

        if os.path.isdir(dir_content) == directories:

            # check if directory starts with number
            result = re.match("^[0-9]+", dir_content)

            if result is not None:

                # remind number at begin
                dirname = result.group()
                directories.append(dir_content)
                no = int(dirname)
                nos.append(no)

    # stop if no directory
    if len(directories) == 0:
        print("No objects available")
        return False

    # find out how many zeros to append
    maximum = max(nos)
    zeros = len(str(maximum))

    # go trough lists to rename objects
    for dir_content in directories:
        result = re.match("^[0-9]+", dir_content)
        pattern = result.group()
        replace = pattern.zfill(zeros)
        new_name = dir_content.replace(pattern, replace)

        # do the renaming
        os.rename(dir_content, new_name)

    return True


def md5sum(filename):
    """Calculates an md5 sum for a given filename."""

    if os.path.exists(filename) is False:
        raise IOError('Path does not exist')

    if os.path.isdir(filename):
        raise ValueError('Path is a directory')

    md5 = hashlib.md5()
    with open(filename, 'rb') as input_file_handle:
        for chunk in iter(lambda: input_file_handle.read(
                128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


def filedatetime():
    """Creates a file-name compatible string of the current date and time."""

    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d'), now.strftime('%H-%M-%S')


def findfiles(path, filter_regex=None, doprint=False, file_limit=0):
    """Lists all files in given directory path recursively."""

    filelist = []
    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            path = os.path.join(dirname, filename)
            if filter_regex is not None:
                match = re.match(filter_regex, path, re.IGNORECASE)
                if match is not None:
                    filelist.append(path)
                    if (doprint):
                        print(path)
                    if file_limit > 0 and len(filelist) >= file_limit:
                        return filelist
            else:
                filelist.append(path)
                if (doprint):
                    print(path)
                if file_limit > 0 and len(filelist) >= file_limit:
                    return filelist
    return filelist


def finddirs(path, doprint=False):
    """ Lists all directories in given directory path recursively."""

    dirlist = []
    for dirname, dirnames, _ in os.walk(path):
        for subdirname in dirnames:
            path = os.path.join(dirname, subdirname)
            dirlist.append(path)
            if (doprint):
                print(path)
    return dirlist


def insertintofilename(filepath, insertion):
    """Append some text between a filename and the file suffix."""

    newfile = ''
    if os.path.dirname(filepath):
        newfile += os.path.dirname(filepath) + os.sep
    newfile += (os.path.basename(os.path.splitext(filepath)[0]) +
                insertion + os.path.splitext(filepath)[1])
    return newfile


def countlines(fname):
    """Counts the lines of the given file"""
    i = -1
    with open(fname) as input_file_handle:
        for i, _ in enumerate(input_file_handle):
            pass
    return i + 1


def getuidfromfilepath(filename):
    """Gets a UID from a filepath"""

    if os.path.exists(filename) is False:
        print("Path does not exist")
        return

    if os.path.isdir(filename):
        print("Path is a directory")
        return

    filename = os.path.basename(filename)
    filename, _ = os.path.splitext(filename)

    return re.sub("[^a-zA-Z0-9_-]", "_", filename)


def basename(path, suffix=None):
    """Basic implementation of Unix basename command with optional suffix"""

    basename = os.path.basename(path)
    if suffix is not None:
        basename = re.sub(suffix + '$', '', basename)
    return basename.strip()


def basename_without_suffix(path):
    """Basic implementation of Unix basename command with suffix removed."""

    bn = basename(path)
    return re.sub('\.[^\.]+$', '', bn).strip()


def file_exists(path):
    """Tests if a file exists"""

    try:
        fobj = open(path)
        fobj.close()
        return True
    except IOError:
        return False


def read_file_to_list(filepath, strip=True, ignore_empty_lines=False):
    """Reads a file and writes content to a list"""

    content = []
    if not file_exists(filepath):
        return content
    ofile = open(filepath)
    for line in ofile:
        if strip:
            line = line.strip()
        if ignore_empty_lines and not line:
            continue
        content.append(line)
    ofile.close()
    return content


def add_to_pythonpath(syspath):
    """Add the given path to system's pythonpath."""
    from os import path
    from sys import path as spath
    if not syspath:
        return
    syspath = path.abspath(syspath)
    if not path.isdir(syspath):
        return
    spath.insert(0, syspath)


def read_file_to_string(filepath, ignore_empty_lines=False):
    """Read file and write content to a string."""
    content = []
    if not file_exists(filepath):
        return content
    ofile = open(filepath)
    for line in ofile:
        line = line.strip()
        if not line and ignore_empty_lines:
            continue
        content.append(line)
    ofile.close()
    return '\n'.join(content)


def write_list_to_file(content, filepath):
    """Writes content of a list to a given file"""

    ofile = open(filepath, 'w')
    for line in content:
        ofile.write(str(line) + '\n')
    ofile.close()


def zip_dir_recursively(base_dir, zip_file):
    """Zip compresses a base_dir recursively"""

    zip_file = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED)
    root_len = len(os.path.abspath(base_dir))
    for root, _, files in os.walk(base_dir):
        archive_root = os.path.abspath(root)[root_len:]
        for f in files:
            fullpath = os.path.join(root, f)
            archive_name = os.path.join(archive_root, f)
            zip_file.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
    zip_file.close()
    return zip_file


def read_config_section_to_keyval_list(config_file, section=None):
    """Takes a configuration config_file and returns a list
    of options for the given or the first section found"""

    items = []
    if not file_exists(config_file):
        print('Config file {0} does not exist'.format(config_file))
        return items

    cp = b_legacy.b_configparser()
    Config = cp()
    try:
        Config.read(config_file)
    except cp.MissingSectionHeaderError:
        print('Config file {0} has no sections'.format(config_file))
        return items

    if section is None:
        section = Config.sections()[0]

    items = Config.items(section)
    return items


def remove_silent(path):
    """Silently remove a file from filesystem. Ignore any errors, especially
    I/O errors when the file does not exist."""

    if path is None:
        return
    try:
        os.remove(path)
    except OSError:
        pass  # catch if file does not exist


def get_file_size(path):
    """Reads the size of the given file path and returns it. If path is
    a directory or file does not exist, method will return None."""

    if not file_exists(path):
        return None
    if os.path.isdir(path):
        return None
    return os.path.getsize(path)


def read_csv_to_array(path, delimiter=';', quotechar='"'):
    """Basic recipe to read a CSV-file to an array of arrays of input fields"""

    import csv
    datasets = []
    if not file_exists(path):
        raise IOError('Input file \'{}\' does not exist.'.format(path))
    with open(path, 'rt') as csvfile:
        csv_datasets = csv.reader(csvfile,
                                  delimiter=delimiter, quotechar=quotechar)
        for csv_dataset in csv_datasets:
            datasets.append(csv_dataset)
    csvfile.close()
    return datasets


def expect_file_argument(directory=False, index=1, add_info=''):
    """A convenience function to request a file or folder argument."""

    from sys import argv, exit
    from os import path
    if len(argv) < (index + 1):
        msg = 'You must provide a {} at option index {}'.format(
            'folder' if directory else 'file', index)
        if add_info and add_info != '':
            msg = '{} ({})'.format(msg, add_info)
        print(msg)
        exit(1)
    return path.abspath(argv[index])


def touch(fname):
    """Touch for python"""

    open(fname, 'a').close()
