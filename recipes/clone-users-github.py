#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Python3 script to clone a user's public github repos and gists."""

from requests import get
from os import path
import json
from sys import exit, argv
from re import sub
from subprocess import call

try:
    argv[1]
except IndexError:
    print('No username provided as first argument!')
    exit(1)

USERNAME = argv[1]

print('CLONING GITHUB CODE FOR USER: {}'.format(USERNAME))
print('\nREPOSITORIES\n')

result = get('https://api.github.com/users/{}/repos?visibility=public'
             .format(USERNAME))
if result.status_code != 200:
    print('Download error.')
    exit(1)
json_entries = json.loads(result.text)
for entry in json_entries:
    full_name = entry['full_name']
    folder_name = sub('{}/'.format(USERNAME), '', full_name)
    url = 'git@github.com:{}.git'.format(full_name)
    print('--- {}'.format(url))
    if not path.isdir(folder_name):
        call(['git', 'clone', url])

print('\nGISTS\n')

call(['mkdir', '-p', '_gists_'])
result = get('https://api.github.com/users/{}/gists?visibility=public'
             .format(USERNAME))
if result.status_code != 200:
    print('Download error.')
    exit(1)
json_entries = json.loads(result.text)
for entry in json_entries:
    folder_name = path.join(
        '_gists_', sub('[^a-zA-Z0-9]', '_', entry['description'][0:60])
        .lower())
    url = 'git@gist.github.com:{}.git'.format(entry['id'])
    print('--- {}'.format(url))
    if not path.isdir(folder_name):
        call(['git', 'clone', url, folder_name])
