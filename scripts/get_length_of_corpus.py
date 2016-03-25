#! /usr/bin/env python

import argparse

from bptbx import b_ffmpeg, b_iotools


FFMPEG_PATH = 'ffmpeg'
CONTENT_PATH = '.'
FILENAME_PATTERN = '.*'

parser = argparse.ArgumentParser(description='Estimate size of an media folder.')
parser.add_argument('-f', metavar='<FFMPEG-BIN>', help='Path to FFMPEG binary (default: ./ffmpeg)')
parser.add_argument('-i', metavar='<FOLDER>', help='Input folder holding media files (default: current)')
parser.add_argument('-p', metavar='<REGEX>', help='Filename regex pattern for file lookup (default: *.*)')
args = parser.parse_args()
  
if not args.f == None:
    FFMPEG_PATH = args.f
if not args.i == None:
    CONTENT_PATH = args.i
if not args.p == None:
    FILENAME_PATTERN = args.p

print 'Using FFMPEG located at: {0}'.format(FFMPEG_PATH)
print 'Using input data in: {0}'.format(CONTENT_PATH)
print 'Filtering input files with pattern: {0}'.format(FILENAME_PATTERN)

ffmpeg = b_ffmpeg.FFMPEG_Handler(FFMPEG_PATH)
mediafiles = b_iotools.findfiles(CONTENT_PATH, FILENAME_PATTERN)

if len(mediafiles) <= 0:
    print 'No files found in respect to given pattern.'
    exit(1)

total_time = []
for mediafile in mediafiles:
    timestamp, milliseconds = ffmpeg.get_file_duration(mediafile)
    print '{0} {1}'.format(mediafile, milliseconds)
    total_time.append(milliseconds)
     
print 'tot-num {0}'.format(len(total_time))
print 'tot-time {0} {1}'.format(b_ffmpeg.convert_milliseconds_to_ffmpeg_timestamp(sum(total_time)), sum(total_time))
print 'avg-time {0} {1}'.format(b_ffmpeg.convert_milliseconds_to_ffmpeg_timestamp(sum(total_time) / len(total_time)), sum(total_time) / len(total_time))
print 'min-time {0} {1}'.format(b_ffmpeg.convert_milliseconds_to_ffmpeg_timestamp(min(total_time)), min(total_time))
print 'max-time {0} {1}'.format(b_ffmpeg.convert_milliseconds_to_ffmpeg_timestamp(max(total_time)), max(total_time))
print 'size_mb@128kbs_mp3 {0}'.format(b_ffmpeg.get_mbsize_for_time_and_kbps (sum(total_time), 128))
print 'size_mb@1411kbs_wav {0}'.format(b_ffmpeg.get_mbsize_for_time_and_kbps (sum(total_time), 1411))
print 'size_mb@450kbs_mp4 {0}'.format(b_ffmpeg.get_mbsize_for_time_and_kbps (sum(total_time), 450))
