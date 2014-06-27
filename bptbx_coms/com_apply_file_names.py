"""
Script for applying a text file holding filenames to a folder containing
a series of subfolders with files in folders.
Layout of textfile must be  

1:    folder_1_file_1
2:    folder_1_file_2
3:    <emptyline>
4:    folder_2_file_1
...
199:  folder_xx_file_xx
EOF//Nonewline

Script will obtain layout from file first, test if layout in folders matches
layout in text file and then applies filenames to files.
"""
from bptbx import b_iotools
from os import path, rename

basefolder = 'c:/basefolder'
filename_txt = 'D:/titles.txt'

general_file_prefix = 'prefix'
begin_with_season = 1

simulate = False

if simulate:
    print 'Will simulate renaming...'

# Parse input file and obtain layout
episodes_p_season = 0
layout = [] 
filenames = []
with open(filename_txt) as input_file_handle:
    for _, line in enumerate(input_file_handle):
        line = line.strip()
        if not line:
            layout.append(episodes_p_season)
            episodes_p_season = 0
        else:
            episodes_p_season += 1
            filenames.append(line.strip())
layout.append(episodes_p_season)

# Print layout in text file
print 'Seasons:', len(layout)
for i, item in enumerate(layout):
    print 'Season', (i + 1), 'has', item, 'episodes'

# Parse folder layout
folders = b_iotools.finddirs(basefolder)
if len(folders) != len(layout):
    print 'More folders [', len(folders), '] found than seasons [', len(layout), '].'
    exit(1)  

# Parse file in folder layout
success = True
for i, folder in enumerate(folders):
    folder = path.abspath(folder)
    files = b_iotools.findfiles(folder)
    if len(files) != layout[i]:
        success = False
        print 'Different number of files [', len(files), '] in', folder, 'found than in layout [', layout[i], '].'

if success is False:
    exit(1)
else:
    print 'Layout check successful!'
    
# Get all current filenames
current_files = b_iotools.findfiles(basefolder)

if len(current_files) == len(filenames):
    print 'Will rename', len(current_files), 'files.'
else:
    print 'Still a mismatch in number of filenames in', filename_txt, 'and', basefolder
    exit(1)

currseason = 0
currepisode = 1
currepperse = layout[currseason]

for i, current_file in enumerate(current_files):
    
    seasonlabel = ''
    if begin_with_season != 0:
        seasonlabel = str(currseason + begin_with_season).zfill(2)
    else:
        seasonlabel = str(currseason + 1).zfill(2)
        
    
    prefix = (general_file_prefix + "_" + "S" + seasonlabel + 
    "E" + str(currepisode).zfill(2) + "-")
    
    current_filepath = path.abspath(current_file)
    base, ext = path.splitext(current_file)
    foldername = path.dirname(current_file)
    new_filepath = path.abspath(foldername + path.sep + prefix + filenames[i] + ext)
    print 'Renaming #', (i + 1), '\nFROM:', current_filepath, '\nTO:  ', new_filepath 
    if not simulate:
        rename(current_filepath, new_filepath)    

    if currepisode == currepperse:
        currseason += 1
        currepisode = 1
        if currseason != len(layout):
            currepperse = layout[currseason]
    else:   
        currepisode += 1
