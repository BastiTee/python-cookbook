#! /usr/bin/env python

"""Not really a test suite but used to test if all modules can be called"""

from platform import system
import traceback
import sys
import random

print '# EXTERNAL DEPENDENCIES (see DEPENDS for details)'
from bptbx.b_iotools import import_modules_with_check, import_module_with_check
message = 'Missing external modules for module \'{0}\': {1}'
# b_web
ext_modules = [ 'ftputil' ]
success, failed_modules = import_modules_with_check(ext_modules)
if success == False:
    print message.format('b_web', failed_modules)

# b_visual
ext_modules = [ 'matplotlib', 'numpy', 'dateutil', 'pyparsing' ]
success, failed_modules = import_modules_with_check(ext_modules)
if success == False:
    print message.format('b_visual', failed_modules)

# b_scan
ext_modules = [ 'reportlab', 'PIL', 'twain' ]
success, failed_modules = import_modules_with_check(ext_modules)
if success == False:
    print message.format('b_scan', failed_modules)

print '#################################\n'
                
def test_cmdline ():
    from bptbx import b_cmdline
    command = ''
    if 'Windows' in system():
        command = 'cd'
    else:
        command = 'ls'
    b_cmdline.checkforcommand(command)
    b_cmdline.runcommand(command, True, True)    
        
def test_enum ():
    from bptbx import b_enum
    my_enum = b_enum.enum ('START', 'STOP')
    assert my_enum.START == 0
    assert my_enum.STOP == 1

def test_iotools():
    from bptbx import b_iotools
    assert (b_iotools.basename('/somewhere/on/the/disc/filetype.css', '.css')
     == 'filetype')
    assert (b_iotools.basename('/somewhere/on/the/disc/filetype.css') 
    == 'filetype.css')
        
def test_ffmpeg ():
    from bptbx import b_cmdline, b_iotools, b_ffmpeg
    ffmpeg_path = 'F:/ffmpeg.exe'
    testfile_path = 'F:/bigbuckbunny.mp4'
    if not b_cmdline.checkforcommand(ffmpeg_path):
        print 'Skipping ffmpeg test. Path {0} not available.'.format(ffmpeg_path)
        return
    if not b_iotools.file_exists(testfile_path):
        print 'Skipping ffmpeg test. Test file {0} not available.'.format(testfile_path)
        return
    ffmpeg_handler = b_ffmpeg.FFMPEG_Handler (ffmpeg_path)
    print ffmpeg_handler.get_file_duration(testfile_path)

def test_math ():    
    from bptbx import b_math
    result = b_math.split_list_to_equal_buckets([1, 2, 3, 4, 5, 6, 7, 8], 3)
    assert result == [[1.0, 2.0, 3.0], [4.0, 5.0], [6.0, 7.0, 8.0]]
        
def test_strings ():
    from bptbx import b_strings
    print b_strings.id_generator()

def random_calculation ():
    val1 = random.randint(1, 100)
    val2 = random.randint(1, 100)
    print 'Calculated: {0} + {1} = {2}'.format(val1, val2, (val1 + val2))

def test_threading ():
    from bptbx import b_threading
    cpus = b_threading.get_cpus()
    print 'Machine has {0} cpus'.format(cpus)
    pool = b_threading.ThreadPool(cpus)
    for _ in range(0, 10):
        pool.add_task(random_calculation)
    print 'Waiting for jobs to be completed'
    pool.wait_completion()

def test_web ():
    success = import_module_with_check('ftputil')
    if success:
        from bptbx import b_web
    else:
        print 'Skipped test for b_web. Missing external imports.'
        return
    content = b_web.download_webpage_to_list('http://www.google.de')
    assert len(content) > 0
    print content[0]

def test_visual ():
    
    ext_modules = [ 'matplotlib', 'numpy', 'dateutil', 'pyparsing' ]
    success, _ = import_modules_with_check(ext_modules)
    if success:
        from bptbx import b_visual
    else:
        print 'Skipped test for b_visual. Missing external imports.'
        return
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
    
    try:
        b_visual.print_dataset(x_axis_dataset, y_axis_datasets,
                y_axis_datalabels, x_axis_isdatetime, title, x_label,
                y_label, fontsize, fontweight, '%d.%m.%Y\n%H:%M', False)
    except NameError:
        pass

if __name__ == "__main__":
    try:
        test_cmdline()
        test_enum()
        test_iotools ()
        test_ffmpeg ()
        test_math()
        test_strings()
        test_threading()
        test_visual()
        test_web() 
    except AssertionError:
        _, _, tb = sys.exc_info()
        
        tbInfo = traceback.extract_tb(tb)
        filename, line, func, text = tbInfo[-1]
        print ('An error occurred on line ' + str(line) + ' in statement ' + text)
        exit(1)
    except Exception as e:
        print 'Exception occurred in test suite: {0}'.format(e)
        exit(1)
    
    print 'Seems everything is alright! See above log for details.'
    exit(0)    
