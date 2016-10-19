#!/usr/bin/env python

from distutils.core import setup
from os import listdir, path

scripts = []
for sfile in listdir('scripts'):
	sfile = path.join('scripts', sfile)
	scripts.append(sfile)
	
setup(
	name='bptbx',
    version='0.2.0',
    description='''Basti\'s Python Toolbox.''',
	long_description='''Basti\'s personal python toolbox for everyday use.''',
    author='Basti Tee',
	author_email='basti.tee@gmx.de',
    url='https://github.com/BastiTee/bastis-python-toolbox',
    packages=['bptbx'],
	package_data={'bptbx': [] },
    scripts=scripts
) 
