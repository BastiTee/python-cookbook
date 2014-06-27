r"""This module contains test scripts to validate toolbox content."""

import os
import re
import sys

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
        
def start ():
    print 'Basti\'s python toolbox is up and running...'
    print 'Install path is {0}'.format(determine_path ())
    print 'Resources included in package:'
    print
    files = [f for f in os.listdir(determine_path () + "/resource")]
    print files
    print
    print 'Available modules and methods and methods:'
    print
    describe_toolbox()
    print
    
if __name__ == "__main__":
    start()
    


