# -*- coding: utf-8 -*-
"""This module contains tools for web connectivity etc."""

DEFAULT_USER_AGENT = ('Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127' +
                      ' Firefox/2.0.0.11')
DEFAULT_ACCEPT = 'text/html'


def download_webpage_to_list(webpage_url, *header_tupels):
    """Download a webpage and writes content into a line-by-line list."""
    from bptbx import b_legacy
    urllib2 = b_legacy.b_urllib2()
    found_ext_accept = False
    found_ext_useragent = False

    opener = urllib2.build_opener()
    headers = []
    for header_tupel in header_tupels:
        headers.append(header_tupel)
        if 'Accept' in header_tupel[0]:
            found_ext_accept = True
        if 'User-Agent' in header_tupel[0]:
            found_ext_useragent = True

    if not found_ext_useragent:
        headers.append(('User-Agent', DEFAULT_USER_AGENT))
    if not found_ext_accept:
        headers.append(('Accept', DEFAULT_ACCEPT))

    opener.addheaders = headers
    input_file_handle = opener.open(webpage_url)
    webpage_url = input_file_handle.readlines()
    input_file_handle.close()
    return webpage_url


def download_file(file_url, target_filepath):
    """Download a file url to a given target filepath."""
    from bptbx import b_legacy
    urllib2 = b_legacy.b_urllib2()
    remote_file = urllib2.urlopen(file_url)
    output = open(target_filepath, 'wb')
    output.write(remote_file.read())
    output.close()


def recursively_download_ftp(host, username, password, ftp_root_path,
                             local_dest_dir):
    """Download from an FTP server to the given target directory."""
    from ftputil import FTPHost
    from re import sub
    from os import path, makedirs

    # Data preparation
    ftp_root_path = sub('\\\\', '/', ftp_root_path)
    ftp_root_path = sub('^[/]*', '/', ftp_root_path)
    ftp_root_path = sub('/$', '', ftp_root_path)

    print('Recursively downloading from ftp://{0}:{1}@{2}{3} to {4}'.format(
        username, password, host, ftp_root_path, local_dest_dir))

    host = FTPHost(host, username, password)
    recursive_file_walk = host.walk(ftp_root_path, topdown=True, onerror=None)
    for folder_path, _, folder_files in recursive_file_walk:

        print('REMOTE DIR\t', folder_path)
        short_folder_path = sub('^' + ftp_root_path, '', folder_path)
        local_folder_path = local_dest_dir
        if short_folder_path:
            local_folder_path = path.join(
                local_dest_dir, sub('^/', '', short_folder_path))
            if not path.exists(local_folder_path):
                makedirs(local_folder_path)
        print('LOCAL DIR\t', local_folder_path)

        if len(folder_files) > 0:
            for folder_file in folder_files:
                remote_path = folder_path + '/' + folder_file
                print('REMOTE FILE\t', remote_path)
                local_file_path = path.join(local_folder_path, folder_file)
                local_file_path = path.abspath(local_file_path)
                print('LOCAL FILE\t', local_file_path)
                host.download_if_newer(remote_path, local_file_path)
        else:
            print('NO FILES')

        print('')

    host.close


def resolve_ip_to_geo_location(ip):
    """Obtain a location for the given IP address via ip-api.com."""
    from time import sleep
    import requests
    import csv
    r = requests.get('http://ip-api.com/csv/{}'.format(ip.strip()))
    if r.status_code != 200:
        print('http-status {} on aquiring geo-location.'.format(
            r.status_code))
        return None
    csv_in = csv.reader([r.text], delimiter=',', quotechar='\"')
    max_requests_per_min = 120  # ip-api.com allows 150 requests per minute
    sleep(60 / max_requests_per_min)  # sleep a little to avoid api limits
    for row in csv_in:
        if row[0].startswith('fail'):
            return [ip, 'fail']
        return [ip] + row


def resolve_ip_list_to_geo_location(ip_list):
    """Obtain locations for the given list of IP addresses."""
    geos = []
    for ip in ip_list:
        if not ip:
            continue
        geo = resolve_ip_to_geo_location(ip)
        if not geo:
            continue
        geos.append(geo)
    return geos


def get_ip_resolver_header():
    """Return the current headers suitable for the data from ip-api.com."""
    return ['ip', 'success', 'country', 'country_code', 'region_code',
            'region_name', 'city', 'zip_code', 'latitude', 'longitude',
            'time_zone', 'isp_name', 'organization_name', 'as_num_name',
            'ip_address_query']

# -----------------------------------------------------------------------------
# MAIN PROPAGATION
# -----------------------------------------------------------------------------


def _main_resolve_ips():
    """Main: Resolve IP addresses via ip-api.com."""
    from sys import exit, argv, stdout
    from bptbx import b_iotools, b_web
    import csv
    if len(argv) <= 1:
        print("No input data provided.")
        exit(1)
    input = argv[1]
    if b_iotools.file_exists(input):
        list = b_iotools.read_file_to_list(input)
        res = [b_web.get_ip_resolver_header()] + \
            b_web.resolve_ip_list_to_geo_location(list)
    else:
        res = [b_web.get_ip_resolver_header()] + \
            [b_web.resolve_ip_to_geo_location(input)]
    writer = csv.writer(stdout, delimiter=',', quotechar='\"',
                        quoting=csv.QUOTE_MINIMAL)
    for row in res:
        writer.writerow(row)
