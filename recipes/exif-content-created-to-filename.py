#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rename files by EXIF Content Created tag."""

import random
import string
from datetime import datetime
from glob import glob
from os import chdir, path, rename
from sys import argv

from exif import Image

if len(argv) < 2:
    print('You need to provide a photo folder.')
    exit(1)

src_folder = path.abspath(argv[1])
chdir(src_folder)

DATE_IN = r'%Y:%m:%d %H:%M:%S'
DATE_OUT = r'%Y%m%d_%H%M%S'

for f_in in glob('./*.jpg'):
    with open(f_in, 'rb') as fh_in:
        im = Image(fh_in)
        datetime_org = datetime.strptime(im.datetime_original, DATE_IN)
        datetime_form = datetime_org.strftime(DATE_OUT)
        rand_string = ''.join(
            random.choice(string.ascii_letters) for i in range(4)
        )
        f_out = f'{datetime_form}_{rand_string}.JPG'
    
    fpath_in = path.join(path.abspath('.'), path.basename(f_in))
    fpath_out = path.join(path.abspath('.'), f_out)
    print(f'{fpath_in} >> {fpath_out}')
    rename(fpath_in, fpath_out)

