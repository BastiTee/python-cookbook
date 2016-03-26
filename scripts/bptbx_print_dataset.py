#! /usr/bin/env python
"""
Script for visualizing a special ping log file and for exampling the usage
of the visual package in conjunction with the math package
"""

from bptbx import b_math
from bptbx import b_strings
from bptbx import b_visual


print '== Initializing script'

INPUTFILE = 'Z:/temp/episode4-ping.log'
MIN_TIMESTAMP = b_strings.timestamp2epoch('2013-05-30 23:00:00.0')
MAX_TIMESTAMP = b_strings.timestamp2epoch('2013-06-07 01:00:00.0')
RESOLUTION = 10000

print 'Input file:    {0}'.format(INPUTFILE)
print 'Earliest date: {0}'.format(b_strings.epoch2timestamp(MIN_TIMESTAMP))
print 'Latest date:   {0}'.format(b_strings.epoch2timestamp(MAX_TIMESTAMP))

response_delay = []
response_delay_filtered = []
response_delay_succ = []
request_timestamp = []

print '== Parsing input file'

with open(INPUTFILE) as input_file_handle:
    for line in input_file_handle:
        line = line.strip()
        test = line.split('\t|')
        timestamp = float(test[0])
        if timestamp >= MIN_TIMESTAMP and timestamp <= MAX_TIMESTAMP:
            if float(test[2]) < 1.0:
                request_timestamp.append(test[0])
                response_delay.append(float(test[2]))
                if test[6] == '0':
                    response_delay_succ.append(test[2])
            else:
                response_delay_filtered.append(float(test[2]))

print 'Total values: {0}'.format(len(response_delay))
print 'Filtered values: {0}'.format(len(response_delay_filtered))
print 'Percent filtered: {0}'.format((float(len(response_delay_filtered))) / (float(len(response_delay))) * 100)
all_response_delays = response_delay + response_delay_filtered
print 'Average response: {0}'.format(sum(all_response_delays) / len(all_response_delays))

print '== Scaling imported data'
        
response_delay_red = b_math.reduce_list(response_delay, RESOLUTION)
response_delay_succ_red = b_math.reduce_list(response_delay_succ, RESOLUTION)
request_timestamp_red = b_math.reduce_list(request_timestamp, RESOLUTION)
timestamps = []
for ts in request_timestamp_red:
    timestamps.append(b_strings.epoch2dtobject(ts))

print '== Visualizing'
    
y_datasets = []
y_datalabels = []
y_datasets.append(response_delay_red)
y_datalabels.append('All requests')
# y_datasets.append(response_delay_succ_red)
# y_datalabels.append('Successful requests')

b_visual.print_dataset(timestamps, y_datasets, y_datalabels, True,
                       'Ping-Status Amazon-Fingerprint System', 'Zeitstempel',
                       'Antwortzeit in s', 10)

