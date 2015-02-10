#! /usr/bin/env python

"""
Postprocess PGN chess games.
"""

import re
import os
import math
import argparse

from bptbx import b_iotools, b_cmdline

# from bptbx.b_iotools import (findfiles, write_list_to_file,
# read_file_to_list, zip_dir_recursively, basename, read_config_section_to_keyval_list)

#############################################################################

USER_FOLDER = os.getcwd()
SE_PATTERNS = []
PGN_EXTRACT = None
PGN_ECO = None
DO_ECO_EXTRACT = False

parser = argparse.ArgumentParser(description='Postprocess PGN chess games.')
parser.add_argument('-i', metavar='<ROOT-FOLDER>',
                    help='Root folder path (default: current location')
parser.add_argument('-p', metavar='<PATTERN-FILE>',
                    help='Search & replace pattern file.')
parser.add_argument('-e', metavar='<PGN-EXTRACT-EXE>',
                    help='Path to optional pgn-extract executable.')
parser.add_argument('-c', metavar='<PGN-EXTRACT-ECO>',
                    help='Path to optional pgn-extract ECO file.')
args = parser.parse_args()

if not args.i == None:
    USER_FOLDER = args.i
if not args.e == None and b_iotools.file_exists(args.e):
    PGN_EXTRACT = args.e
if not args.c == None and b_iotools.file_exists(args.c):
    PGN_ECO = args.c
if not PGN_EXTRACT == None and not PGN_ECO == None:
    DO_ECO_EXTRACT = True 
if not args.p == None:
    SE_PATTERNS = b_iotools.read_config_section_to_keyval_list(args.p)
else:
    print 'No pattern search & replace file detected.'
    
print SE_PATTERNS
print 'Applying {0} search & replace patterns'.format(len(SE_PATTERNS))
print 'PGN Extract active: {0}. Set to "{1}" with ECO-file "{2}"'.format(DO_ECO_EXTRACT, PGN_EXTRACT, PGN_ECO)

FULL_PLAYBOOK_NAME = 'full-playbook'
STATS_NAME = 'full-stats'
STATS_PATH = os.path.join(USER_FOLDER, STATS_NAME) + '.txt'
FULL_PLAYBOOK_PATH = os.path.join(USER_FOLDER, FULL_PLAYBOOK_NAME) + '.pgn'
PLAYERS = {}    
FIRST_GAME = True
GAME_DATA = []
ZIP_NAME = 'Spielearchiv.zip'

#############################################################################

def find_last_metadata_index (data):
    i = 1
    lastidx = i
    for line in data:
        if re.match('^[ ]*\[.*', line, re.IGNORECASE):
            lastidx = i 
        i = i + 1
    return lastidx    

def strip_formatting (string):
    string = re.sub('^[^\"]+\"', '', string)
    string = re.sub('\".*', '', string)
    return string.strip()
                
def apply_fixes (line):
    if SE_PATTERNS is None:
        return line
    for SE_PATTERN in SE_PATTERNS:
        newline = re.sub(SE_PATTERN[0], SE_PATTERN[1], line, flags=re.IGNORECASE)
        if not newline == line:
            print 'pattern {0} matched on {1}'.format(SE_PATTERN[0], line)
            line = newline
            break
    return line

def apply_filename_pattern ():
    
    ifiles = b_iotools.findfiles(USER_FOLDER, '.*\\.(pgn|PGN)$')
    print 'found {0} pgn files for renaming'.format(len(ifiles))
    
    used_names = []
    
    for ifile in ifiles:
        
        white = ''
        black = ''
        date = ''
        res = ''
        iterator = 1
        
        if ((not FULL_PLAYBOOK_NAME in os.path.abspath(ifile)) and
        (not '_Analysis_' in os.path.abspath(ifile))):
            content = b_iotools.read_file_to_list(ifile)
            # Extract filename information
            for line in content:
                if ('[White' in line and not 'WhiteElo' in line):
                    white = re.sub(',.*', '', strip_formatting(line))
                    white = white.lower()
                if ('[Black' in line and not 'BlackElo' in line):
                    black = re.sub(',.*', '', strip_formatting(line))
                    black = black.lower()
                if '[Date' in line:
                    date = re.sub(',.*', '', strip_formatting(line))
                    date = re.sub('\\.', '_', date)
                if '[Result' in line:
                    res = re.sub(',.*', '', strip_formatting(line))
                    res = re.sub('1/2-1/2', '0.5-0.5', strip_formatting(res))
                
            # Generate target filename
            
            while True:
                run = str(iterator).zfill(3)
                iterator = iterator + 1
                trg_filename = '{0}_{1}-{2}_{3}_#{4}'.format(date,
                                      white, black, res, run)    
                if not trg_filename in used_names:
                    used_names.append(trg_filename)
                    break
            
            trg_filename = '{0}.pgn'.format(trg_filename)
            
            # Generate target folder name
            src_filename = os.path.abspath(ifile)
            trg_folder = os.path.abspath(os.path.join(src_filename, os.pardir))
            trg_filename = os.path.join(trg_folder, trg_filename)
            
            if src_filename != trg_filename:
                print 'Renaming: {0} --> {1}'.format(
                b_iotools.basename(src_filename),
                b_iotools.basename(trg_filename))                
                os.rename(src_filename, trg_filename)

#############################################################################

elo_numbers = {}

def get_elo_from_elo_list (name):
    try:
        elo = elo_numbers[name] 
        return elo
    except KeyError:
        return 1200

def set_elo_on_elo_list (name, elo):
    elo_numbers[name] = elo
    
def calculate_elo (player_a, player_b, point):
    elo_a = get_elo_from_elo_list(player_a.name)
    elo_b = get_elo_from_elo_list(player_b.name)
    rev_point = abs(point - 1)
    E_a = 1.0 / (1.0 + math.pow(10, (float(elo_b) - float(elo_a)) / 400))
    E_b = 1.0 - E_a
    point = float(point)
    elo_a_new = elo_a + 10 * (point - E_a) 
    elo_b_new = elo_b + 10 * (rev_point - E_b)
    elo_a_new = int(round(elo_a_new, 0))
    elo_b_new = int(round(elo_b_new, 0))
    set_elo_on_elo_list(player_a.name, elo_a_new)
    set_elo_on_elo_list(player_b.name, elo_b_new)

class PlayerStat:
    
    games_total = 0.0
    games_white = 0.0
    games_black = 0.0

    points_total = 0.0
    points_white = 0.0
    points_black = 0.0
    
    winrate_total = 0.0
    winrate_white = 0.0
    winrate_black = 0.0
    
    def __init__(self, name):
        self.name = name
        self.opponents = {}
        
    def get_name (self):
        return self.name
    
        
    
    def add_point (self, point, white, opponents_name):

        # Catch scoring for ties
        if (point == '1/2'):
            point = 0.5
        point = float(point)
        
        # Add general stats 
        self.games_total += 1.0
        self.points_total += point
    
        # Add player relative stats 
        if white == True:
            self.games_white += 1.0
            self.points_white += point
        else:
            self.games_black += 1.0
            self.points_black += point
                   
        self.update_averages()
        
        # Update opponent list
        if not opponents_name == None:
            try:
                opponent = self.opponents[opponents_name]
            except KeyError:
                opponent = PlayerStat(opponents_name)
                self.opponents[opponents_name] = opponent
            opponent.add_point(point, white, None)
            
            # Update ELO
            if white == True:
                calculate_elo(self, opponent, point)
            
    def update_averages (self):
        try:
            self.winrate_total = self.points_total / self.games_total
        except ZeroDivisionError: 
            pass
        try:
            self.winrate_black = self.points_black / self.games_black
        except ZeroDivisionError: 
            pass
        try:
            self.winrate_white = self.points_white / self.games_white
        except ZeroDivisionError: 
            pass


def handle_result_data (GAME_DATA):
    wplayer = None
    bplayer = None
    for line in GAME_DATA:
        if '[White ' in line:
            name = strip_formatting(line)
            try:
                wplayer = PLAYERS[name]
            except KeyError:
                wplayer = PlayerStat(name)
                PLAYERS[name] = wplayer

        if '[Black ' in line:
            name = strip_formatting(line)
            try:
                bplayer = PLAYERS[name]
            except KeyError:
                bplayer = PlayerStat(name)
                PLAYERS[name] = bplayer
                
        if '[Result ' in line:
            result = strip_formatting(line)
            result_split = result.split('-')
            wplayer.add_point(result_split[0], True, bplayer.get_name())
            bplayer.add_point(result_split[1], False, wplayer.get_name())

#############################################################################

print 'will use files in folder {0}'.format(USER_FOLDER)
ifiles = b_iotools.findfiles(USER_FOLDER, '.*\\.(pgn|PGN)')
print 'found {0} pgn files'.format(len(ifiles))
iterator = 1
full_data = {}
date = ''

i = 0
for ifile in ifiles:
    if (not FULL_PLAYBOOK_NAME in os.path.abspath(ifile) and 
        not '_Analysis_' in os.path.abspath(ifile)):
        content = b_iotools.read_file_to_list(ifile)
        found_eco = False
        found_round = False
        fixed_content = []
        for line in content:
            if re.match('[ ]*\[[ ]*ECO.*',line, re.IGNORECASE):
                found_eco = True
            if re.match('[ ]*\[[ ]*Round.*',line, re.IGNORECASE):
                line = re.sub('\?', '1', line)
                found_round = True
            if re.match('^[ ]*\[[ ]*Event[ ]*\"\?\"[ ]*\]',line, re.IGNORECASE):
                line = '[Event "Freizeitspiel"]'
            if 'Date' in line:
                date = strip_formatting(line) + '_' + str(iterator).zfill(3)
                iterator += 1
            fixed_line = apply_fixes(line)
            fixed_content.append(fixed_line)
        
        if not found_round:
            idx = find_last_metadata_index(fixed_content)
            fixed_content.insert(idx, '[Round "1"]')
        if not found_eco:
            if DO_ECO_EXTRACT:
                idx = find_last_metadata_index(fixed_content)
                _, stdouts, _ = b_cmdline.runcommand('{0} -e{1} {2}'.format(PGN_EXTRACT, PGN_ECO, ifile), True, True)
                for stdout in stdouts:
                    if '[ECO' in stdout:
                        fixed_content.insert(idx, stdout)
                    if '[Opening' in stdout:
                        fixed_content.insert(idx, stdout)
            
        full_data[date] = fixed_content
        b_iotools.write_list_to_file(fixed_content, ifile)
        i = i + 1
        
    else:
        print 'ignored file {0}'.format(ifile)

print 'found {0} valid pgn files'.format(i)
if i == 0:
    print 'nothing to do. will exit'
    exit()
    
print 'creating reversed full playbook for statistics'
full_playbook_reverse = []
full_playbook = []
for key in sorted(full_data.iterkeys(), None, None, False):
    for line in full_data[key]:
        full_playbook_reverse.append(line)
    full_playbook_reverse.append('')

print 'creating non-reversed full playbook for printing'    
for key in sorted(full_data.iterkeys(), None, None, True):
    for line in full_data[key]:
        full_playbook.append(line)
    full_playbook.append('')
b_iotools.write_list_to_file(full_playbook, FULL_PLAYBOOK_PATH)

print 'creating stats'
for line in full_playbook_reverse:
    if '[Event' in line:
        if FIRST_GAME == True:
            FIRST_GAME = False
        else:
            handle_result_data (GAME_DATA) 
            GAME_DATA = []
    
    if ('[White ' in line or 
         '[Black ' in line or 
         '[Result ' in line):
        GAME_DATA.append(line)
handle_result_data (GAME_DATA) 
GAME_DATA = []

print 'outputting stats'

def add_to_output (player, output, tab=''):    
    output.append('{0}name:          {1}'.format(tab, player.name))
    output.append('{0}games_total:   {1}'.format(tab, player.games_total))
    output.append('{0}games_white:   {1}'.format(tab, player.games_white))
    output.append('{0}games_black:   {1}'.format(tab, player.games_black))

    output.append('{0}points_total:  {1}'.format(tab, player.points_total))
    output.append('{0}points_white:  {1}'.format(tab, player.points_white))
    output.append('{0}points_black:  {1}'.format(tab, player.points_black))
    
    output.append('{0}winrate_total: {1}'.format(tab, player.winrate_total))
    output.append('{0}winrate_white: {1}'.format(tab, player.winrate_white))
    output.append('{0}winrate_black: {1}'.format(tab, player.winrate_black))
    output.append('')

stat_content = []
for key in PLAYERS.keys():
    player = PLAYERS[key]
    stat_content.append('======================================')
    add_to_output(player, stat_content)
    stat_content.append('\t=== Opponents =============\n')
    for key2 in player.opponents.keys():
        opp = player.opponents[key2]
        add_to_output(opp, stat_content, '\t')
stat_content.append('\nELO-Ratings:')
for key in elo_numbers:
    stat_content.append('{0}\t{1}'.format(elo_numbers[key], key))

b_iotools.write_list_to_file(stat_content, STATS_PATH)

apply_filename_pattern ()

print 'zipping folder for backup'
b_iotools.zip_dir_recursively(USER_FOLDER, os.path.join(os.path.join(
                    USER_FOLDER, '..'), ZIP_NAME))
