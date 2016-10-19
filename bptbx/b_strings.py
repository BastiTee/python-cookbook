r"""This module contains various tools for string operations."""

from datetime import datetime
import random
from re import sub
import string
import time


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """This method creates a random string with given length and given
    allowed characters"""

    return ''.join(random.choice(chars) for _ in range(size))

def fillzeros (number, desiredlength=1):
    return (str(number).zfill(desiredlength))

def epoch2timestamp (epoch, formatstring='%Y-%m-%d %H:%M:%S.%f'):
    """Converts an epoch/unix time string to a timestamp"""

    timestamp = epoch2dtobject(epoch, formatstring).strftime(formatstring)
    return timestamp

def epoch2dtobject (epoch, formatstring='%Y-%m-%d %H:%M:%S.%f'):
    """Converts an epoch/unix time string to a datetime object"""

    timestamp = datetime.fromtimestamp(float(epoch))
    return timestamp

def timestamp2dtobject (timestamp, formatstring='%Y-%m-%d %H:%M:%S.%f'):
    """"Converts a timestamp to a datetime object"""

    dtobj = datetime.strptime(timestamp, formatstring)
    return dtobj

def timestamp2epoch (timestamp, formatstring='%Y-%m-%d %H:%M:%S.%f'):
    """Converts a timestamp to an epoch/unix time string"""

    datetimeobj = timestamp2dtobject(timestamp, formatstring)
    epoch = (time.mktime(datetimeobj.timetuple()) +
             float(datetimeobj.microsecond) / 1000000)
    return epoch

def concat_list_to_string (input_list, separator=''):
    """Concatenates a input_list of elements to a string with the given separator.
       All objects within the input_list will be parsed as String"""
    if input_list == None:
        return ''
    returnstring = ''
    for element in input_list:
        returnstring = returnstring + str(element) + separator
    return sub(separator + '$', '', returnstring)

def get_current_datetime_for_filename ():
    """Returns a date & time timestamp that can be used for filenames"""

    st = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H%M%S')
    return st

def get_current_date_for_filename ():
    """Returns a date timestamp that can be used for filenames"""

    st = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    return st
