#! /usr/bin/env python

"""
Script to operate bastis python toolbox from the command line
"""

from b_iotools import findfiles, basename
from b_cmdline import runcommand
import inspect
import os

tools = {}
COM_EXIT = 'x'
COM_PRINT_MENU = 'm'

def print_awesome_header ( working_path ):
    print 'Working path = {0}'.format(working_path)
    print '   _________         _________'
    print '  /         \       /         \   BASTI\'s'
    print ' /  /~~~~~\  \     /  /~~~~~\  \  PYTHON TOOLBOX'
    print ' |  |     |  |     |  |     |  |'
    print ' |  |     |  |     |  |     |  |'
    print ' |  |     |  |     |  |     |  |         /'
    print ' |  |     |  |     |  |     |  |       //'
    print '(o  o)    \  \_____/  /     \  \_____/ /'
    print ' \__/      \         /       \        /'
    print '  |         ~~~~~~~~~         ~~~~~~~~'
    print '  ^'

def print_menu ():
    print
    for num, _ in enumerate(tools):
        print '{0}:\t{1}'.format(num, basename(tools[num]))
    print '\n'+COM_PRINT_MENU+':\tPrint this menu'
    print COM_EXIT+':\tExit\n'
    
def check_if_valid_command( command ):
    # Get first argument 
    com_split = command.split()
    if not com_split is None:
        # Try to look up in tool list
        try:
            tool_name = tools[int(com_split[0])]
            # Replace tool index with actual tool path
            com_split[0] = '"'+tool_name+'"'
            command = ' '.join(com_split)
            return True, command
        except KeyError:
            # Handle error on unknown key
            return False, command
    

def start ():
    # Setup menu
    working_file = inspect.getfile(inspect.currentframe())
    working_path =  os.path.abspath(working_file)
    print_awesome_header(working_path)
    toolbox_content = findfiles(os.path.dirname(working_path), '.*\\.py$')
    com_num = 0
    for script in toolbox_content:
        if (not '__init__' in script and not 
            basename(working_file) in script):
            tools[com_num] = script
            com_num = com_num + 1
    # Print menu
    print_menu()
    # Go into infinite loop and serve user commands
    while True:
        print "<BPT>: ",
        command = raw_input()
        command = command.strip()
        if command == COM_EXIT:
            exit()
        elif command == COM_PRINT_MENU:
            print_menu()
        else:
            if command != '':
                valid, command = check_if_valid_command(command)
                if valid == True:
                    # Execute command
                    print 'Executing: {0}'.format(command)
                    runcommand(command, False, False, True)
                else:
                    print 'Unknown command'
        
if __name__ == "__main__":
    start()