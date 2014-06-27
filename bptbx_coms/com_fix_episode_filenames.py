"""
Script for renaming legally downloaded TV-episodes by extracting all 
available information from the given filename, looking up metadata in
the web, creating a new filen name and finally renaming that file. 
"""

from bptbx import b_iotools
from bptbx import b_web

import re
import os
import tempfile
import argparse

#############################################################################

# USER PROPERTIES
# Base folder for processing
user_folder = 'D:/Download/'
user_doit = False
# CONSTANTS
# Filter pattern for relevant file suffixes
ALLOWED_SUFFIXES = '(mp4|MP4|avi|AVI)'
SUFFIX_PATTERN = '.*\\.{0}'.format(ALLOWED_SUFFIXES)
# Pattern to clean out file names
CLEAN_PATTERN = '(EVOLVE)|(HDTV)|(LOL)|(VTV)|(KILLERS)|(REPACK)|(2HD)|(x264)'
EPISODE_PATTERN = '[Ss]?[0-9]{1,2}[EeXx][0-9]{1,2}'
COUNT_PATTERN = '[\d]{1,2}'
TVRAGE_SEARCH = 'http://services.tvrage.com/feeds/search.php?show={0}'
TVRAGE_LOOKUP = 'http://services.tvrage.com/feeds/episode_list.php?sid={0}'
FILENAME_PATTERN = '{0}_S{1}E{2}-{3}.{4}'
FILENAME_CONVERTED_PATTERN = ''

#############################################################################

# DATASET HELPER CLASS
class Dataset:
    filename = ''
    series = ''
    season = ''
    episode = ''
    new_fname = ''
    title = ''
    
    def __init__(self, filename, series=None, season=None, episode=None):
        self.filename = filename
        self.series = series
        self.season = season
        self.episode = episode
        
    def found_infos (self):
        if self.filename == None:
            return False
        if self.episode == None:
            return False
        if self.season == None:
            return False
        if self.series == None:
            return False
        return True

def filter_already_converted_filenames (my_list):
    
    filtered_list = []
    for my_file in my_list:
        bname = b_iotools.basename(my_file)
        if re.match('.*(' + CLEAN_PATTERN + ').*', bname, re.IGNORECASE):
            print bname
            print '\tContains strings typical for not converted my_file'
            filtered_list.append(my_file)
            continue
        
    return filtered_list

#############################################################################

parser = argparse.ArgumentParser(description='Rename legally downloaded TV-series files with own pattern.')
parser.add_argument('-i', metavar='<INPUT-FOLDER>', help='Input folder path')
parser.add_argument('-doit', action='store_true', help='Do the actual renaming', default='False')
args = parser.parse_args()

if args.i == None:
    print 'You need to set the input folder'
    parser.print_help()
    exit()

user_folder = args.i
user_doit = args.doit

step = 1

print 'will use files in folder {0}'.format(user_folder)
print 'step {0}:\tobtain files from folder'.format(step)
step = step + 1
ifiles = b_iotools.findfiles(user_folder, SUFFIX_PATTERN)
print '\tfound {0} files to work with'.format(len(ifiles))

print 'step {0}:\tfilter already converted files'.format(step)
step = step + 1
ifiles = filter_already_converted_filenames (ifiles)
print '\tfound {0} files to work with'.format(len(ifiles))

print 'step {0}: extracting info from file names'.format(step)
step = step + 1

datasets = []
unknown_files = []
serieslist = []
for ifile in ifiles:
    ifile = os.path.abspath(ifile)
    season = None
    episode = None
    series = None
        
    bn = b_iotools.basename(ifile)
    bn = re.sub('\\.[^\\.]+$', '', bn)
    bn_clean = re.sub(CLEAN_PATTERN, '', bn)
    match = re.search(EPISODE_PATTERN, bn_clean)
    if not match == None:
        season_episode = str(match.group(0))
        se_ep_list = re.findall(COUNT_PATTERN, season_episode)
        if len(se_ep_list) == 2:
            season = re.sub('^0+', '', se_ep_list[0])
            episode = re.sub('^0+', '', se_ep_list[1])
            series = re.sub(season_episode + '.*$', '', bn_clean)
            series = re.sub('_', ' ', series)
            series = re.sub('[^\w]', ' ', series).strip().lower()
            if series not in serieslist:
                serieslist.append(series)
                
    dataset = Dataset(ifile, series, season, episode)
    
    if dataset.found_infos() == True:
        datasets.append(dataset)
    else:
        unknown_files.append(dataset.filename)
        
print '\tcould not find infos for {0} files:'.format(len(unknown_files))
for unknown_file in unknown_files:
    print '\t' + unknown_file
    
print 'step {0}: finding wiki pages for series'.format(step)
step = step + 1
serieswikis = {}
for series in serieslist:
    wikisite = None
    url = TVRAGE_SEARCH.format(series)
    url = re.sub(' ', '+', url)
    content = b_web.download_webpage_to_list(url)
    for line in content:
        line = line.strip()
        if 'showid' in line:
            line = re.sub('<[^>]+>', '', line)
            wikisite = TVRAGE_LOOKUP.format(line)
            serieswikis[series] = wikisite
            break    
    print '\t{0} -> {1}'.format(series, wikisite)
    
print 'step {0}: downloading wikipages for episodes'.format(step)
step = step + 1
fds = []
for series in serieswikis.keys():
    fd, tmpfile = tempfile.mkstemp('bptb_', 'html')
    fds.append(fd)
    b_web.download_file(serieswikis[series], tmpfile)
    serieswikis[series] = tmpfile

print 'step {0}: finding info for episodes'.format(step)
step = step + 1   
for dataset in datasets:
    ref_lines = b_iotools.read_file_to_list(serieswikis[dataset.series])
    correct_season = False
    for ref_line in ref_lines:
        ref_line = ref_line.strip()
        match = re.match('.*<Season no=\"[0]*' + dataset.season + '\">.*', ref_line)
        if not match == None:
            correct_season = True
        if correct_season == True:
            if not re.match('.*<seasonnum>[0]*' + dataset.episode + '</seasonnum>.*', ref_line) == None:
                title = re.sub ('.*<title>', '', ref_line)
                title = re.sub ('<\/title>.*', '', title)
                dataset.title = title
                break
        
print 'step {0}: creating target filenames'.format(step)
step = step + 1    
for dataset in datasets:
    stitle = dataset.series.title()
    if stitle == "":
        continue
    etitle = dataset.title.title()
    if etitle == "":
        continue
    se = str(dataset.season).zfill(2)
    ep = str(dataset.episode).zfill(2)
    suff = re.sub('.*\\.', '', dataset.filename)
    filename = stitle + '_S' + se + 'E' + ep + '-' + etitle + '.' + suff
    filename = re.sub(' ', '_', filename)
    filename = re.sub('[/\\\]', '_', filename)
    filename = re.sub('[?]', '', filename)
    parent = os.path.abspath(os.path.join(dataset.filename, os.pardir))
    dataset.new_fname = os.path.join(parent, filename)

print 'step {0}: applying filenames:'.format(step)
step = step + 1
for dataset in datasets:
    print ''
    print 'From: ' + dataset.filename
    print 'To:   ' + dataset.new_fname
    if dataset.new_fname is "":
        print 'New filename not obtained. Nothing to do.'
    else:
        if user_doit == True:
            os.rename(dataset.filename, dataset.new_fname)
    
print '\nstep {0}: cleaning up'.format(step)
step = step + 1
for fd in fds:
    os.close(fd)
for series in serieswikis.keys():
    tfile = serieswikis[series]
    print '\tremoving temp file at {0}'.format(tfile)
    os.remove(tfile)

print 'step {0}: done...'.format(step)
step = step + 1    
if user_doit == False:
    print '\tto rename files for real start with -doit option'
