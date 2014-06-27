r"""This module contains FFMPEG and Audio/Video related functions."""

import re
import b_cmdline
import b_iotools

class FFMPEG_Handler:
    """Python handler binding for ffmpeg"""
    
    FFMPEG_PATTERN = '{0} -i {1} {2}'
    
    def __init__(self, ffmpeg_executable_path='ffmpeg', verbose=False):
        self.suppress = True
        if verbose == True:
            self.suppress = False
        self.ffmpeg_path = ffmpeg_executable_path
        initcommand = self.ffmpeg_path + ' -version'
        code, out, _ = b_cmdline.runcommand(initcommand, self.suppress, self.suppress)
        if code is not 0:
            raise IOError('FFMPEG not available at location \'{0}\''.format(ffmpeg_executable_path)) 
        else:
            if self.suppress == False:
                for o in out:
                    if 'ffmpeg version' in o:
                        print 'Successfully initialized {0}'.format(o)
        
        
    def get_file_duration(self, filepath):
        """Returns the duration of the given media filepath as ffmpeg timestamp and in milliseconds"""
        
        if not b_iotools.file_exists(filepath):
            raise IOError('Given filepath {0} does not exist!'.format(filepath))
        command = self.FFMPEG_PATTERN.format(self.ffmpeg_path, filepath, '')
        _, _, err = b_cmdline.runcommand(command, self.suppress, self.suppress)
        dur_line = None
        for e in err:
            if 'Duration: ' in e:
                dur_line = e
        if dur_line is None:
            raise IOError('FFMPEG Error. Consider using verbose-mode for more details.') 
        logline_split = dur_line.split(' ')
        duration_string = re.sub(',.*', '', logline_split[1]) 
        return duration_string, convert_ffmpeg_timestamp_to_milliseconds(duration_string)

def convert_ffmpeg_timestamp_to_milliseconds (timestamp):
    """Converts a timestamp of form hh:mm:ss.fff to a millisecond integer representation"""
    
    tmp = re.sub('[^0-9]', ' ', timestamp)
    split = tmp.split(' ')
    total_time = 0
    if len(split) == 4:
        split[3] = split[3].ljust(3, '0')
        total_time += int(split[3])
    total_time = total_time + (int(split[2]) * 1000)
    total_time = total_time + (int(split[1]) * 1000 * 60)
    total_time = total_time + (int(split[0]) * 1000 * 60 * 60)
    return total_time

def convert_milliseconds_to_ffmpeg_timestamp (milliseconds):
    """Converts a millisecond integer representation to a timestamp of form hh:mm:ss.fff"""
    
    tmp = int(milliseconds)
    mse = tmp % 1000
    tmp = (tmp - mse) / 1000
    sec = tmp % 60  
    tmp = (tmp - sec) / 60
    mnt = tmp % 60
    hrs = (tmp - mnt) / 60
    timestamp = '{0}:{1}:{2}.{3}'.format(str(hrs).zfill(2), str(mnt).zfill(2), str(sec).zfill(2), str(mse).zfill(3))
    return timestamp

def get_mbsize_for_time_and_kbps (time_ms, bitrate_kbps):
    """Calculates the megabyte size of av data given a length in milliseconds and a bitrate in kilobits per second"""
    
    sec = float(time_ms) / 1000
    size_kbits = sec * bitrate_kbps
    size_mb = size_kbits / 8 / 1024
    return size_mb
