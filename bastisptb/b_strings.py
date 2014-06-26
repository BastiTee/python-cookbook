r"""This module contains various tools for string operations."""

import string
from re import sub
import random
from datetime import datetime
import time

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """This method creates a random string with given length and given 
    allowed characters"""
    
    return ''.join(random.choice(chars) for _ in range(size))

def convert_seconds_to_timestamp ( timecode ):

    sec = int(timecode)
    sec =  sec % 60
    secs = str(sec).zfill(2)
    mini = (int(timecode) / 60) % 60
    minis = str(mini).zfill(2)
    hrs = (int(timecode) / 60 / 60) % 24
    hrss = str(hrs).zfill(2)
    timestamp = hrss + "_" + minis + "_" + secs
    
    return timestamp
    
def fillzeros ( number, desiredlength=1):
    print str(number).zfill(desiredlength)
    
def epoch2timestamp ( epoch, formatstring='%Y-%m-%d %H:%M:%S.%f'):
    """Converts an epoch/unix time string to a timestamp"""
        
    timestamp = epoch2dtobject(epoch, formatstring).strftime(formatstring)
    return timestamp

def epoch2dtobject ( epoch, formatstring='%Y-%m-%d %H:%M:%S.%f'):
    """Converts an epoch/unix time string to a datetime object"""
        
    timestamp = datetime.fromtimestamp(float(epoch))
    return timestamp 

def timestamp2dtobject ( timestamp, formatstring='%Y-%m-%d %H:%M:%S.%f'):
    """"Converts a timestamp to a datetime object"""
        
    dtobj = datetime.strptime(timestamp, formatstring)    
    return dtobj 

def timestamp2epoch ( timestamp, formatstring='%Y-%m-%d %H:%M:%S.%f'):
    """Converts a timestamp to an epoch/unix time string"""
    
    datetimeobj = timestamp2dtobject(timestamp, formatstring)
    epoch = (time.mktime(datetimeobj.timetuple()) + 
             float(datetimeobj.microsecond)/1000000)
    return epoch 

def concat_list_to_string ( list, separator='' ):
    """Concatenates a list of elements to a string with the given separator.
       All objects within the list will be parsed as String"""
    if list == None:
        return ''
    returnstring = ''
    for element in list:
        returnstring = returnstring + str(element) + separator  
    return sub(separator+'$', '', returnstring)

def get_current_datetime_for_filename ():
    """Returns a date & time timestamp that can be used for filenames"""
    
    st = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H%M%S')
    return st

def get_current_date_for_filename ():
    """Returns a date timestamp that can be used for filenames"""
    
    st = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    return st
