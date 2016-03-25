#! /usr/bin/env python

"""
Scans a folder for image files and creates a thumbnail version to allow
fast skimming of the image folder.
"""

import argparse
from os import path
import re
import shutil
from threading import Lock

from bptbx import b_iotools, b_pil, b_threading


#############################################################################
FILE_PATTERN = re.compile('^.*\\.(jpg|jpeg|gif|png){1}$')
INDEX_IMAGE_LONG_SIDE_PX = 400.0
DEBUG = False
MAX_THREADS = 100

parser = argparse.ArgumentParser(description='Create an image index.')
parser.add_argument('-i', metavar='<INPUT-FOLDER>',
                    help='Root path of image folder hierarchy')
parser.add_argument('-o', metavar='<OUTPUT-FOLDER>',
                    help='Target root path for image index')
args = parser.parse_args()

if not args.i:
    parser.error('Input folder not set.')
if not args.o:
    parser.error('Output folder not set.')
if not path.exists(args.i):
    parser.error('Input folder does not exist.')
if not path.exists(args.o):
    parser.error('Output folder does not exist.')

args.i = path.abspath(args.i)
args.o = path.abspath(args.o)

#############################################################################

directories = b_iotools.finddirs(args.i)
directories.append(args.i)
print 'found {0} directories...'.format(len(directories))
total_images = len(b_iotools.findfiles(args.i, FILE_PATTERN))
print 'found {0} files...'.format(total_images)

current_dir = 1
current_file = 1
print_lock = Lock()

def print_process_file_status ():
    global current_file 
    print_lock.acquire()
    try:
        print '\tfile {0}/{1} done'.format(current_file, total_images)
        current_file = current_file + 1
    finally:
        print_lock.release() #

def process_file (f_from, f_to):
    
    long_side_px = b_pil.get_length_of_long_side(f_from)
    factor = INDEX_IMAGE_LONG_SIDE_PX / float(long_side_px)
    if not b_iotools.file_exists(f_to):
        b_pil.resize_image_with_factor(f_from, f_to, factor)
    
    if DEBUG:
        print '\t\t{0} -->\n\t\t{1}'.format(f_from, f_to)
                 
    print_process_file_status()

def copy_file (f_from, f_to):
    shutil.copy(f_from, f_to)

def recursive_file_walk (directory, thread_pool = None):
    global current_dir
    curr_dir_abs = path.join(args.i, directory)
    curr_trg_dir_abs = path.join (args.o, directory)
    if DEBUG:
        print '--\t{0} -->\n  \t{1}'.format(curr_dir_abs, curr_trg_dir_abs)
    b_iotools.mkdirs(curr_trg_dir_abs)
    
    images = b_iotools.get_immediate_subfiles(curr_dir_abs)
    for image in images:
        if re.match(FILE_PATTERN, image.lower()):
            f_from = path.join(curr_dir_abs, image)
            f_to = path.join(curr_trg_dir_abs, image) 
    
            #if not thread_pool:
            if not b_iotools.file_exists(f_to):
                copy_file (f_from, f_to) 
            #else:
            #    thread_pool.add_task(process_file, f_from, f_to)   
    
    print 'dir {0}/{1} done...'.format(current_dir, len(directories))
    current_dir = current_dir + 1

    # step through subdirs           
    subdirs = b_iotools.get_immediate_subdirectories(curr_dir_abs)
    for subdir in subdirs:
        recursive_file_walk (path.join(directory, subdir), thread_pool)     
    
thread_pool = b_threading.ThreadPool(MAX_THREADS)
recursive_file_walk('', thread_pool)
thread_pool.wait_completion()