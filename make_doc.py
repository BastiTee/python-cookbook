"""A script using epydoc to generate a Javadoc-like API documentation
of all the toolbox core modules"""

import sys

from bptbx.b_iotools import import_module_with_check
from epydoc import cli


success = import_module_with_check ('epydoc')
if not success:
    print 'Cannot generate documentation. You need to install epydoc first!'
    exit(1) 


sys.argv = ['epydoc', '--html', '-o', 'bptbx_doc', '--name',
            'Basti\'s Python Toolbox', '--url',
            'http://github.com/BastiTee/bastis-python-toolbox', 'bptbx']
options, names = cli.parse_arguments()
cli.main(options, names)
