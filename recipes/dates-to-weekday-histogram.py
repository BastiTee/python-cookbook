#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import stdin, argv, exit
from bptbx import b_date

try:
    date_time_format = argv[1]
except IndexError:
    print('No date-time format provided.')
    exit(1)

res_map = {}

for line in stdin:
    if not line:
        continue
    line = line.strip()
    if 'epoch' in date_time_format:
        dto = b_date.epoch_to_dto(line)
    else:
        dto = b_date.timestamp_to_dto(line, date_time_format)
    weekday = int(dto.strftime('%w'))
    if weekday == 0:  # make sunday the 7th day like jebuz would
        weekday = 7
    try:
        res_map[weekday]
    except KeyError:
        res_map[weekday] = {
            '00': 0, '01': 0, '02': 0, '03': 0, '04': 0, '05': 0,
            '06': 0, '07': 0, '08': 0, '09': 0, '10': 0, '11': 0,
            '12': 0, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0,
            '18': 0, '19': 0, '20': 0, '21': 0, '22': 0, '23': 0,
        }
    # if dto.strftime("%H") == "00":
    #     hourofday = "24"
    # else:
    hourofday = dto.strftime("%H")
    curr_val = res_map[weekday][hourofday]
    res_map[weekday][hourofday] = curr_val + 1

print('day,hour,value')
for key in res_map.keys():
    vals = sorted(list(res_map[key].keys()))
    for val in vals:
        print('{},{},{}'.format(key, val, res_map[key][val]))
