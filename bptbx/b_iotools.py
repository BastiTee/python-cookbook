r"""This module contains various tools for recurring I/O operations."""

import os
import re
import hashlib
import datetime
import b_enum
import zipfile

def appendzeros (directory, filetype):
    """Appends leading zeros to all files or directories in given 
    directory path if theses objects have leading numbers."""  
     
    if (filetype is not b_enum.Filetype.FILE and 
    filetype is not b_enum.Filetype.DIR):
        print "Argument 'filetype' must be of type b_enum.Filetype"        
        return False
    
    # list all directory content
    folders = os.listdir(directory)
    
    # create an array of signed integers
    nos = []
    directories = []
    
    for direc in folders:
        
        usedirs = True
        if filetype is b_enum.Filetype.FILE:
            usedirs = False
        
        if os.path.isdir(direc) == usedirs:
            
            # check if directory starts with number 
            result = re.match("^[0-9]+", direc)
            
            if result is not None:
                
                # remind number at begin
                dirname = result.group()
                directories.append(direc)
                no = int(dirname)
                nos.append(no)
    
    # stop if no directory
    if len(directories) == 0:
        print "No objects available"
        return False
           
    # find out how many zeros to append     
    maximum = max(nos)
    zeros = len(str(maximum))
    
    # go trough lists to rename objects
    for direc in directories:
        result = re.match("^[0-9]+", direc)
        pattern = result.group()
        replace = pattern.zfill(zeros)
        new_name = direc.replace(pattern, replace)
        
        # do the renaming
        os.rename(direc, new_name)
        
    return True


def md5sum (filename):
    """Calculates an md5 sum for a given filename."""
    
    if os.path.exists(filename) is False:
        raise IOError ('Path does not exist')
    
    if os.path.isdir(filename):
        raise ValueError('Path is a directory')
    
    md5 = hashlib.md5()
    with open(filename, 'rb') as input_file_handle: 
        for chunk in iter(lambda: input_file_handle.read(
                        128 * md5.block_size), b''): 
            md5.update(chunk)
    return md5.hexdigest()

def filedatetime ():
    """Creates a file-name compatible string of the current date and time."""
    
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d'), now.strftime('%H-%M-%S')
    
def findfiles (path, filter_regex=None, doprint=False):
    """Lists all files in given directory path recursively."""
        
    filelist = []
    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            path = os.path.join(dirname, filename)
            if filter_regex != None:
                match = re.match(filter_regex, path)
                if match != None:
                    filelist.append(path)
                    if (doprint): 
                        print path
            else:
                filelist.append(path)
                if (doprint): 
                    print path
    return filelist
         
def finddirs (path, doprint=False):
    """ Lists all directories in given directory path recursively."""
         
    dirlist = []       
    for dirname, dirnames, _ in os.walk(path):
        for subdirname in dirnames:
            path = os.path.join(dirname, subdirname)
            dirlist.append(path)
            if (doprint):
                print path
    return dirlist
    

def insertintofilename (filepath, insertion):
    """Append some text between a filename and the file suffix."""
     
    newfile = (os.path.dirname(filepath) + os.sep + 
    os.path.basename(os.path.splitext(filepath)[0]) + 
    insertion + os.path.splitext(filepath)[1])
    return newfile
    
def countlines (fname):
    """Counts the lines of the given file"""
    i = -1
    with open(fname) as input_file_handle:
        for i, _ in enumerate(input_file_handle):
            pass
    return i + 1
   
def getuidfromfilepath (filename):
    """Gets a UID from a filepath"""
    
    if os.path.exists(filename) is False:
        print "Path does not exist"
        return
    
    if os.path.isdir(filename):
        print "Path is a directory"
        return
    
    filename = os.path.basename(filename)
    filename, _ = os.path.splitext(filename)
    
    return re.sub("[^a-zA-Z0-9_-]", "_", filename)

def basename (path, suffix=None):
    """Basic implementation of Unix basename command with optional suffix"""
    
    basename = os.path.basename(path)
    if suffix is not None:
        basename = re.sub(suffix + '$', '', basename)
    return basename

def file_exists (path):
    """Tests if a file exists"""
    
    try:
        with open(path):
            return True
    except IOError:
        return False
            
def read_file_to_list (filepath):
    """Reads a file and writes content to a list"""
    
    content = []
    ofile = open (filepath)
    for line in ofile:
        line = line.strip()
        content.append(line)
    ofile.close()
    return content   
    
def write_list_to_file (content, filepath):
    """Writes content of a list to a given file"""
    
    ofile = open (filepath, 'w')
    for line in content:
        ofile.write(str(line) + '\n')
    ofile.close()

def zip_dir_recursively (dir, zip_file):
    """Zip compresses a directory recursively"""
    
    zip = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED)
    root_len = len(os.path.abspath(dir))
    for root, dirs, files in os.walk(dir):
        archive_root = os.path.abspath(root)[root_len:]
        for f in files:
            fullpath = os.path.join(root, f)
            archive_name = os.path.join(archive_root, f)
            zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
    zip.close()
    return zip_file
