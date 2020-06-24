"""This module contains various tools for recurring I/O operations."""

import csv
import datetime
import hashlib
import os
import re
import zipfile
from os import path
from sys import path as spath


def change_to_scriptdir(file):
    """Change to the folder where the script resides.

    For current script call with change_to_scriptdir(__file__)
    """
    os.chdir(os.path.dirname(os.path.abspath(file)))


def mkdirs(directory):
    """Create directory structure if it does not exist."""
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
    """Return the direct sub-directories of a given file path."""
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
    """Return the direct sub-files of a given file path."""
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
    """Check if a given set of modules exists."""
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
    """Check if a given module exists. If yes, import it."""
    module_names = [module]
    success, _ = import_modules_with_check(module_names)
    return success


def appendzeros(directory, directories=False):
    """Append leading zeros to all files or directories.

    Only applied if theses objects have leading numbers.
    """
    # list all directory content
    dir_contents = os.listdir(directory)

    # create an array of signed integers
    nos = []
    directories = []

    for dir_content in dir_contents:

        if os.path.isdir(dir_content) == directories:

            # check if directory starts with number
            result = re.match('^[0-9]+', dir_content)

            if result is not None:

                # remind number at begin
                dirname = result.group()
                directories.append(dir_content)
                no = int(dirname)
                nos.append(no)

    # stop if no directory
    if len(directories) == 0:
        print('No objects available')
        return False

    # find out how many zeros to append
    maximum = max(nos)
    zeros = len(str(maximum))

    # go trough lists to rename objects
    for dir_content in directories:
        result = re.match('^[0-9]+', dir_content)
        pattern = result.group()
        replace = pattern.zfill(zeros)
        new_name = dir_content.replace(pattern, replace)

        # do the renaming
        os.rename(dir_content, new_name)

    return True


def md5sum(filename):
    """Calculate an md5 sum for a given filename."""
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
    """Create a file-name compatible string of the current date and time."""
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d'), now.strftime('%H-%M-%S')


def findfiles(path_string, filter_regex=None, doprint=False, file_limit=0):
    """List all files in given directory path recursively."""
    filelist = []
    for dirname, _, filenames in os.walk(path_string):
        for filename in filenames:
            file_path = os.path.join(dirname, filename)
            if filter_regex is not None:
                match = re.match(filter_regex, file_path, re.IGNORECASE)
                if match is not None:
                    filelist.append(file_path)
                    if (doprint):
                        print(file_path)
                    if file_limit > 0 and len(filelist) >= file_limit:
                        return filelist
            else:
                filelist.append(file_path)
                if (doprint):
                    print(file_path)
                if file_limit > 0 and len(filelist) >= file_limit:
                    return filelist
    return filelist


def finddirs(file_path, doprint=False):
    """List all directories in given directory path recursively."""
    dirlist = []
    for dirname, dirnames, _ in os.walk(file_path):
        for subdirname in dirnames:
            file_path = os.path.join(dirname, subdirname)
            dirlist.append(path)
            if (doprint):
                print(path)
    return dirlist


def insertintofilename(filepath, insertion):
    """Append some text between a filename and the file suffix."""
    newfile = ''
    if os.path.dirname(filepath):
        newfile += os.path.dirname(filepath) + os.sep
    newfile += (os.path.basename(os.path.splitext(filepath)[0])
                + insertion + os.path.splitext(filepath)[1])
    return newfile


def countlines(fname):
    """Count the lines of the given file."""
    i = -1
    with open(fname) as input_file_handle:
        for i, _ in enumerate(input_file_handle):
            pass
    return i + 1


def getuidfromfilepath(filename):
    """Get a UID from a filepath."""
    if os.path.exists(filename) is False:
        print('Path does not exist')
        return

    if os.path.isdir(filename):
        print('Path is a directory')
        return

    filename = os.path.basename(filename)
    filename, _ = os.path.splitext(filename)

    return re.sub('[^a-zA-Z0-9_-]', '_', filename)


def basename(path, suffix=None):
    """Get basename command with optional suffix."""
    basename = os.path.basename(path)
    if suffix is not None:
        basename = re.sub(suffix + '$', '', basename)
    return basename.strip()


def basename_without_suffix(path):
    """Get basename command with suffix removed."""
    bn = basename(path)
    return re.sub(r'\.[^\.]+$', '', bn).strip()


def file_exists(path):
    """Test if a file exists."""
    try:
        fobj = open(path)
        fobj.close()
        return True
    except IOError:
        return False


def read_file_to_list(filepath, strip=True, ignore_empty_lines=False):
    """Read a file and writes content to a list."""
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
    """Write content of a list to a given file."""
    ofile = open(filepath, 'w')
    for line in content:
        ofile.write(str(line) + '\n')
    ofile.close()


def zip_dir_recursively(base_dir, zip_file):
    """Zip compresses a base_dir recursively."""
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


def remove_silent(file_path):
    """Silently remove a file from filesystem. Ignore any errors."""
    if file_path is None:
        return
    try:
        os.remove(file_path)
    except OSError:
        pass  # catch if file does not exist


def get_file_size(file_path):
    """Read the size of the given file path and returns it.

    If path is a directory or file does not exist, method will return None.
    """
    if not file_exists(file_path):
        return None
    if os.path.isdir(file_path):
        return None
    return os.path.getsize(file_path)


def read_csv_to_array(csv_path, delimiter=';', quotechar='"'):
    """Read a CSV - file to an array of arrays of input fields."""
    datasets = []
    if not file_exists(csv_path):
        raise IOError(f'Input file \'{csv_path}\' does not exist.')
    with open(csv_path, 'rt') as csvfile:
        csv_datasets = csv.reader(csvfile,
                                  delimiter=delimiter, quotechar=quotechar)
        for csv_dataset in csv_datasets:
            datasets.append(csv_dataset)
    csvfile.close()
    return datasets


def touch(fname):
    """Touch for python."""
    open(fname, 'a').close()
