#!/usr/bin/env python3
"""A ZIP-file pretending to be a filesystem folder.

A code example of how to work with a ZIP-file transparently acting as a
filesystem folder. This code uses the pyfilesystem2 library by
Will McGugan. See: https://github.com/PyFilesystem/pyfilesystem2.
"""

from os import path, remove
from sys import argv

from fs import copy, osfs, zipfs

# setup a fs-object using ZipFS
target_filepath = 'sample.zip'
target_file = zipfs.ZipFS(target_filepath, 'w')

# setup a hook to the OS filesystem using OSFS
source_dir = osfs.OSFS('.')

# manually write file
target_file.settext(
    'README.txt',
    'Hello World!'
)

# create subdir
target_file.makedirs('sub1/sub2')

# copy this script into the archive
copy.copy_file(source_dir, path.basename(argv[0]),
               target_file, 'sub1/sub2/test.py')

# obtain a file handle for later usage
with target_file.open('iterator.txt', 'w') as it_file:
    for i in range(5):
        it_file.write(str(i) + '\n')

# list all files
print()
for filename in target_file.walk.files():
    print(filename)

# print tree
print()
target_file.tree()

# print readme
print()
with target_file.open('README.txt') as testfile:
    print(testfile.read())

# print another file
print()
with target_file.open('iterator.txt') as testfile:
    print(testfile.read())

# finalize and cleanup
target_file.close()
remove(target_filepath)
