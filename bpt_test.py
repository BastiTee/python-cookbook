#! /usr/bin/env python

'''Not really a test suite but used to test if all modules can be called'''

# Toolbox imports 
from bptbx import b_cmdline
from bptbx import b_enum
from bptbx import b_ffmpeg
from bptbx import b_iotools
from bptbx import b_math
from bptbx import b_strings
from bptbx import b_threading
from bptbx import b_visual
from bptbx import b_web

# External imports 
from platform import system
import traceback
import sys
import random
import os
import re

def determine_path ():
    try:
        root = __file__
        if os.path.islink (root):
            root = os.path.realpath (root)
        return os.path.dirname (os.path.abspath (root))
    except:
        print "I'm sorry, but something is wrong."
        print "There is no __file__ variable. Please contact the author."
        sys.exit ()
    
def describe_toolbox ():
    """This method prints all available modules and methods in this toolbox"""
    
    path = determine_path()
    modulelist = []
    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            path = os.path.join(dirname, filename)
            match = re.match('b_.*\\.py$', filename)
            if match != None:
                modulelist.append(path)
    
    for module in modulelist:
        print '== {0}'.format(re.sub('.*b_', 'b_', module))
        ofile = open (module)
        for line in ofile:
            match = re.search("^def ", line)
            if match is not None:
                line = re.sub("^def ", "", line)
                line = re.sub(":[ ]*$", "", line)
                print '   {0}'.format(line.strip())
                
def test_cmdline ():
	command = ''
	if 'Windows' in system():
		command = 'cd'
	else:
		command = 'ls'
	b_cmdline.checkforcommand(command)
	b_cmdline.runcommand(command)    
        
def test_enum ():
	my_enum = b_enum.enum ('START', 'STOP')
	assert my_enum.START == 0
	assert my_enum.STOP == 1
	
def test_iotools():
	assert b_iotools.basename('/somewhere/on/the/disc/filetype.css', '.css') == 'filetype'
	assert b_iotools.basename('/somewhere/on/the/disc/filetype.css') == 'filetype.css'
        
def test_ffmpeg (ffmpeg_path, testfile_path):
	if not b_cmdline.checkforcommand(ffmpeg_path):
		print 'Skipping ffmpeg test. Path {0} not available.'.format(ffmpeg_path)
		return
	if not b_iotools.file_exists(testfile_path):
		print 'Skipping ffmpeg test. Test file {0} not available.'.format(testfile_path)
		return
	ffmpeg_handler = FFMPEG_Handler (ffmpeg_path)
	print ffmpeg_handler.get_file_duration(testfile_path)

def test_math ():	
	result = b_math.split_list_to_equal_buckets([1, 2, 3, 4, 5, 6, 7, 8], 3)
	assert result == [[1.0, 2.0, 3.0], [4.0, 5.0], [6.0, 7.0, 8.0]]
        
def test_strings ():
	print b_strings.id_generator()
	
def random_calculation ():
	val1 = random.randint(1, 100)
	val2 = random.randint(1, 100)
	print 'Calculated: {0} + {1} = {2}'.format(val1, val2, (val1 + val2))

def test_threading ():
	cpus = b_threading.get_cpus()
	print 'Machine has {0} cpus'.format(cpus)
	pool = b_threading.ThreadPool(cpus)
	for x in range(0, 10):
		pool.add_task(random_calculation)
	print 'Waiting for jobs to be completed'
	pool.wait_completion()

def test_web ():
    content = b_web.download_webpage_to_list('http://www.google.de')
    assert len(content) > 0
    print content[0]

def test_visual ():
    
    x_axis_dataset = []
    y1 = []
    y2 = []
    for x in range(1, 11):
        x_axis_dataset.append(x)
        y1.append(random.randint(1, 100))
        y2.append(random.randint(1, 100))
    y_axis_datasets = [y1, y2]
    y_axis_datalabels = ['Some data', 'Some other data']
    x_axis_isdatetime = False
    title = 'Test plot'
    x_label = 'Data points'
    y_label = 'Random values'
    fontsize = 9
    fontweight = 'bold'
    
    b_visual.print_dataset(x_axis_dataset, y_axis_datasets, y_axis_datalabels, x_axis_isdatetime, title, x_label,
                           y_label, fontsize, fontweight, '%d.%m.%Y\n%H:%M', False)

if __name__ == "__main__":
    try:
        test_cmdline()
        test_enum()
        test_iotools ()
        test_ffmpeg ('F:/ffmpeg.exe', 'F:/bigbuckbunny.mp4')
        test_math()
        test_strings()
        test_threading()
        test_visual()
        test_web()
        print 'Basti\'s python toolbox is up and running...'
        print 'Install path is {0}'.format(determine_path ())
        print 'Available modules and methods and methods:'
        describe_toolbox()    
        
    except AssertionError:
        _, _, tb = sys.exc_info()
        
        tbInfo = traceback.extract_tb(tb)
        filename, line, func, text = tbInfo[-1]
        print ('An error occurred on line ' + str(line) + ' in statement ' + text)
    except Exception as e:
        print 'Exception occured in test suite: {0}'.format(e)
        raise
