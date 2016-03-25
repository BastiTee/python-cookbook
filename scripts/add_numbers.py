"""
A very simple test script that adds two numbers. Used for testing. 
"""

import argparse


parser = argparse.ArgumentParser(description='Add two numbers')
parser.add_argument('-a', metavar='<Number A>', help='First number argument')
parser.add_argument('-b', metavar='<Number B>', help='Second number argument')
args = parser.parse_args()

if args.a == None:
    print 'You need to set number A'
    parser.print_help()
    exit()
    
if args.b == None:
    print 'You need to set number B'
    parser.print_help()
    exit()
    
try:
    result = float(args.a) + float(args.b)
    print '\n{0} + {1} = {2}'.format(args.a, args.b, result)
except ValueError:
    print 'You need to input numerical arguments!'
    parser.print_help()
    exit()
