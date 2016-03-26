#!/usr/bin/env python
"""
A script to recursively download an ftp folder to a local folder.  
"""

import argparse

from bptbx import b_web


def print_help (message=''):
    print message
    parser.print_help()
    exit()

parser = argparse.ArgumentParser(description='Recursively download ftp folder')
parser.add_argument('-f', metavar='<HOSTNAME>', help='FTP Hostname')
parser.add_argument('-u', metavar='<USERNAME>', help='FTP Username')
parser.add_argument('-p', metavar='<PASSWORD>', help='FTP Password')
parser.add_argument('-i', metavar='<REMOTE_PATH>', help='Remote source path')
parser.add_argument('-o', metavar='<TARGET_PATH>', help='Local target path')
args = parser.parse_args()

FTP_HOST = args.f
FTP_USER = args.u
FTP_PASS = args.p
FTP_ROOT_PATH = args.i
DEST_DIR = args.o

if FTP_HOST == None:
    print_help('FTP_HOST unset')

if FTP_USER == None:
    print_help('FTP_USER unset')
    
if FTP_PASS == None:
    print_help('FTP_PASS unset')
    
if FTP_ROOT_PATH == None:
    print_help('FTP_ROOT_PATH unset')
    
if DEST_DIR == None:
    print_help('DEST_DIR unset')    

b_web.recursively_download_ftp (FTP_HOST, FTP_USER, FTP_PASS, FTP_ROOT_PATH, DEST_DIR)
