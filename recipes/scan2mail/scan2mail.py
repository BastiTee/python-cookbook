#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bptbx import b_shell, b_iotools, b_mail, b_date
from argparse import ArgumentParser
from time import sleep, time as _time
from datetime import datetime
from sys import exit
from shutil import rmtree
from os import chdir, path
from json import load
from re import match, IGNORECASE

WORKFLOW_NAME = 'scan2mail'

# -----------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------


def log(*message):
    """Print given message along with the current timestamp."""
    if not message:
        return
    now = datetime.fromtimestamp(_time()).strftime('%d.%m.%Y %H:%M:%S |')
    print(now, ' '.join(map(str, message)))


def wdir(c, *subpaths):
    """Short alias to obtain the absolute working path."""
    return path.join(c['workdir'], WORKFLOW_NAME, *subpaths)


def get_input_files(c):
    """Obtain a list of all valid input files."""
    in_files = b_iotools.get_immediate_subfiles(
        path.join(c['workdir']), pattern='.*\.(jpg|jpeg)', ignorecase=True)
    return in_files, len(in_files)


def synchronize_owncloud(c, run_once=False):
    """Perform synchronization to owncloud/nextcloud endpoint."""
    if c.get('skip_owncloud', False):
        return
    while True:  # We will do this until the run did not yield any new files
        _, len_fin = get_input_files(c)
        log('Updating owncloud to', c['workdir'])
        log('+', len_fin, 'input files present before update')
        silent = '-s' if not c.get('oc_verbose', False) else ''
        cmd = ('owncloudcmd {} -h {} https://{}:{}@{}/remote.php/webdav/{}'
               .format(silent, c['workdir'], c['oc_user'], c['oc_pass'], c['oc_host'],
                       c['oc_folder']))
        if not silent:
            log(cmd)
        b_shell.exe(cmd)
        _, len_fin_new = get_input_files(c)
        log('+', len_fin_new, 'input files present after update')
        # check if the number of files has changed
        if len_fin_new == len_fin or run_once:
            return
        sleep(10)


def extract_by_filename_pattern(c, file):
    """Extract information via filename."""
    # default android pattern, e.g., IMG_20180202_072813.jpg
    if match('^img_[0-9]{8}_[0-9]{6}\.(jpg|jpeg)$', file, IGNORECASE):
        bn = b_iotools.basename_without_suffix(file)
        return datetime.strptime(bn, 'IMG_%Y%m%d_%H%M%S').strftime('%s')

    # Here one could extend with more recurring patterns...

    return None


def extract_epoch_by_exif(c, file):
    """Extract information via EXIF information."""
    _, stdout, _ = b_shell.exe('identify -verbose {}'.format(
        path.join(c['workdir'], file)), None, True, True)
    stdout = list(filter(lambda x: 'date:modify' in x, stdout))
    if len(stdout) < 1:
        return 0
    # and save it to the resulting list
    exif_ts = stdout[0].split(': ')[1].strip()[:19]
    epoch_ts = datetime.strptime(
        exif_ts, '%Y-%m-%dT%H:%M:%S').strftime('%s')
    return epoch_ts


def setup_uptodate_create_dates(c, files, create_dates):
    """Create a list of up-to-date create dates for the given files."""
    new_create_dates = []
    for file in files:
        bn = b_iotools.basename_without_suffix(file)
        # checck if we calculated the creation time before
        date_present = None
        for create_date in create_dates:
            if bn in create_date:
                date_present = create_date
        if date_present:
            new_create_dates.append(date_present)
            continue
        # if not found read the creation time from somewhere
        # fastest and on android pretty safe is to check for filename pattern
        epoch_ts = extract_by_filename_pattern(c, file)
        # if not use exif
        if not epoch_ts:
            epoch_ts = extract_epoch_by_exif(c, file)
        ts = b_date.epoch_to_timestamp(epoch_ts, '%d.%m.%Y_%H:%M:%S')
        new_create_dates.append(epoch_ts + ' ' + ts + ' ' + bn)
    return new_create_dates


def partition_timestamps(list_ts):
    """Partition given list of timestamps.

    This algorithm will take an unordered list of integers representing
    epoch timestamps and tries to find harmonic partitions for it. Harmonic
    means that timestamps in the same partition are close to each other
    compared to the remaining timestamps. If the time difference is bigger
    than MAX_DIFFERENCE_IN_S then the timestamps will be considered as separate
    partitions.
    """
    MAX_DIFFERENCE_IN_S = 60
    list_ts = [int(ts) for ts in list_ts]
    list_ts.sort()

    # go through input list and calculate distance between elements
    ts_diffs = [list_ts[i] - list_ts[i - 1]
                for i, ts in enumerate(list_ts) if i > 0]

    # create result list and append first original item to first partition
    res_list_ts = [[list_ts[0]]]
    list_pt = 0

    # calculate new partitions (this is trivial atm since it only considers
    # the max difference as criterion)
    for i, ts_diff in enumerate(ts_diffs):
        if ts_diff > MAX_DIFFERENCE_IN_S:
            list_pt += 1
            res_list_ts.append([])
        res_list_ts[list_pt].append(list_ts[i + 1])

    return res_list_ts


def calculate_file_batches(infile):
    """Take a list of files/timestamps and find best file batches."""
    try:
        fh_in = open(infile)
    except FileNotFoundError:
        return []
    # setup batches data structure
    batches = []
    for line in fh_in.readlines():
        if not line.strip():
            continue
        split = line.strip().split(' ')
        batches.append([' '.join(split[2:]), int(split[0]), split[1]])
    fh_in.close()
    batches.sort(key=lambda x: x[1])
    # run packaging algorithm
    ts_list = partition_timestamps([b[1] for b in batches])
    batches_packed = []
    shift = 0
    for i, ts_sublist in enumerate(ts_list):
        batch = i + 1
        for b in batches[shift:(shift + len(ts_sublist))]:
            batches_packed.append([batch] + b)
        shift += len(ts_sublist)
    # [print(b) for b in batches_packed]
    return batches_packed


def send_mail(c, new_documents):
    """Send a mail for each new document."""
    log('Sending new PDFs to mail account')
    for new_document in new_documents:
        log('+ sending {} with account {} to {}'
            .format(path.basename(new_document), c['mail_account'],
                    c['mail_recipient']))
        if c.get('skip_mailing', False):
            continue
        b_mail.send_mail(
            c['mail_account'], c['mail_recipient'],
            WORKFLOW_NAME +
            ' - Your scan is ready!', path.basename(new_document),
            c['mail_account'], c['mail_pass'], c['mail_host'], new_document)


# -----------------------------------------------------
# MAIN WORKFLOW
# -----------------------------------------------------


def run_toolchain(c):
    # -----------------------------------------------------
    c['workdir'] = path.abspath(c['workdir'])
    b_iotools.mkdirs(c['workdir'])
    chdir(c['workdir'])
    for subdir in ['in', 'tif', 'pdf', 'docs', 'meta']:
        b_iotools.mkdirs(wdir(c, subdir))

    # -----------------------------------------------------
    synchronize_owncloud(c)

    # -----------------------------------------------------
    log('Strip input files')
    files, _ = get_input_files(c)
    for file in files:
        bn = b_iotools.basename_without_suffix(file)
        tf = wdir(c, 'in', bn + '.jpg')
        ff = path.join(c['workdir'], file)
        if not b_iotools.file_exists(tf):
            b_shell.exe('convert {} -auto-orient -strip {}'.format(ff, tf))

    # -----------------------------------------------------
    log('Converting input files to tif')
    files = b_iotools.get_immediate_subfiles(
        wdir(c, 'in'), pattern='.*\.(jpg)', ignorecase=True)
    for file in files:
        bn = b_iotools.basename_without_suffix(file)
        tf = wdir(c, 'tif', bn + '.tif')
        if not b_iotools.file_exists(tf):
            b_shell.exe('scantailor-cli -l=1 {} {}'.format(
                wdir(c, 'in', file), wdir(c, 'tif')))
    rmtree(wdir(c, 'tif', 'cache'), ignore_errors=True)

    # -----------------------------------------------------
    log('Converting tif to pdf')
    files = b_iotools.get_immediate_subfiles(
        wdir(c, 'tif'), pattern='.*\.(tif)', ignorecase=True)
    for file in files:
        bn = b_iotools.basename_without_suffix(file)
        tf = wdir(c, 'pdf', bn + '.pdf')
        if not b_iotools.file_exists(tf):
            b_shell.exe(
                'tiff2pdf -p A4 -F -o {} {}'.format(tf, wdir(c, 'tif', file)))

    # -----------------------------------------------------
    log('Calculating file batches')
    files, _ = get_input_files(c)
    # load previously calculated timestamps
    create_dates = b_iotools.read_file_to_list(
        wdir(c, 'meta', 'create-dates.txt'))
    new_create_dates = setup_uptodate_create_dates(c, files, create_dates)

    # write creation time file only if we obtained new timestamps
    if sorted(new_create_dates) != sorted(create_dates):
        b_iotools.write_list_to_file(
            new_create_dates, wdir(c, 'meta', 'create-dates.txt'))
    batches = calculate_file_batches(wdir(c, 'meta', 'create-dates.txt'))

    # -----------------------------------------------------
    log('Creating final pdfs')
    new_documents = []
    batch = 1
    while True:
        # Go through each batch
        batch_content = [b for b in batches if b[0] == batch]
        if len(batch_content) == 0:
            break
        out_file = wdir(c, 'docs', batch_content[0][1] + '_scan.pdf')
        in_files = ' '.join([wdir(c, 'pdf',
                                  s[1] + '.pdf') for s in batch_content])
        in_files_short = ' '.join([s[1] + '.pdf' for s in batch_content])
        log('+ batch:   {}'.format(batch))
        log('+ files:   {}'.format(in_files_short))
        log('+ output:  {}'.format(path.basename(out_file)))
        batch += 1
        if not b_iotools.file_exists(out_file):
            b_shell.exe('pdftk {} cat output {}'.format(in_files, out_file))
            new_documents.append(out_file)
        else:
            log('+ FILE EXISTS!')

    # -----------------------------------------------------
    send_mail(c, new_documents)
    synchronize_owncloud(c, True)


# -----------------------------------------------------
# MAIN
# -----------------------------------------------------

if __name__ == '__main__':
    missing_tools = b_shell.available_list(
        ['scantailor-cli', 'pdftk', 'tiff2pdf',
         'convert', 'identify', 'owncloudcmd'])
    if len(missing_tools) > 0:
        print('You need to install missing tools ({}) first.'
              .format(', '.join(missing_tools)))
        exit(1)
    # Parse command line
    prs = ArgumentParser(WORKFLOW_NAME)
    prs.add_argument('-i', required=True, action='append',
                     metavar='CONFIG_FILE', help='Configuration file')
    args = prs.parse_args()

    cwd = path.dirname(path.abspath(__file__))
    cfiles = []
    for cfile in args.i:
        if not b_iotools.file_exists(cfile):
            print('Configuration file does not exist:', cfile)
            exit(1)
        cfile = path.abspath(cfile)
        cfiles.append(cfile)
        log('Configuration file', cfile, 'present.')
    try:
        for cfile in cfiles:
            log('-------- CONFIG:', cfile)
            chdir(cwd)
            run_toolchain(load(open(cfile)))
        log('-- finished scan2mail run.')
        exit(0)
    except Exception as e:
        from traceback import print_exc
        log('---------------------------')
        log('!!! UNEXPECTED ERROR:, ', e)
        print_exc()
        log('---------------------------')
