#! /usr/bin/env python

'''Not really a test suite but used to test if all modules can be called'''

from bptbx import b_cmdline
from bptbx import b_strings
from platform import system

def test_cmdline ():
	if 'Windows' in system():
		
    print b_strings.id_generator()
        
def test_strings ():
	print b_strings.id_generator()
		
if __name__ == "__main__":

	print system()
	test_cmdline()