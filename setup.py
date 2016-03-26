#!/usr/bin/env python

from distutils.core import setup

from os import listdir, path

sfiles = []
for sfile in listdir('scripts'):
	sfile = path.join('scripts', sfile)
	sfiles.append(sfile)
	
setup(
	name='bptbx',
    version='0.1.0',
    description='''Basti\'s python toolbox.''',
	long_description='''Basti\'s personal python toolbox for everyday use.''',
    author='Basti Tee',
	author_email='basti.tee@gmx.de',
    url='https://github.com/BastiTee/bastis-python-toolbox',
    packages=['bptbx'],
	package_data={'bptbx': ['*.txt']},
    scripts=sfiles
) 
