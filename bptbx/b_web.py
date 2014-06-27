r"""This module contains tools for web connectivity etc."""

from urllib2 import build_opener, urlopen
from re import sub
from os import path, makedirs
from ftputil import FTPHost

DEFAULT_USER_AGENT = ('Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127' +
                      ' Firefox/2.0.0.11')
DEFAULT_ACCEPT = 'text/html'

def download_webpage_to_list (webpage_url, *header_tupels):
    """Downloads a webpage and writes content into a line-by-line list."""  
    
    found_ext_accept = False
    found_ext_useragent = False
    
    opener = build_opener()
    headers = []
    for header_tupel in header_tupels:
        headers.append(header_tupel)
        if 'Accept' in header_tupel[0]:
            found_ext_accept = True
        if 'User-Agent' in header_tupel[0]:
            found_ext_useragent = True
    
    if found_ext_useragent == False:
        headers.append(('User-Agent', DEFAULT_USER_AGENT))
    if found_ext_accept == False:
        headers.append(('Accept', DEFAULT_ACCEPT))
    
    opener.addheaders = headers
    input_file_handle = opener.open(webpage_url)
    webpage_url = input_file_handle.readlines()
    input_file_handle.close()
    return webpage_url

def download_file (file_url, target_filepath):
    """Downloads a file url to a given target filepath."""  
    remote_file = urlopen(file_url)
    output = open(target_filepath, 'wb')
    output.write(remote_file.read())
    output.close()
    
def recursively_download_ftp (host, username, password, ftp_root_path, 
                              local_dest_dir):
    
    # Data preparation
    ftp_root_path = sub ('\\\\', '/', ftp_root_path)
    ftp_root_path = sub ('^[/]*', '/', ftp_root_path)
    ftp_root_path = sub('/$', '', ftp_root_path)
    
    print 'Recursively downloading from ftp://{0}:{1}@{2}{3} to {4}'.format(
                username, password, host, ftp_root_path, local_dest_dir)
    
    
    host = FTPHost(host, username, password)
    recursive = host.walk(ftp_root_path, topdown=True, onerror=None) 
    for folder_path, _, folder_files in recursive:
    
        print 'REMOTE DIR\t', folder_path
        short_folder_path = sub('^' + ftp_root_path, '', folder_path)
        local_folder_path = local_dest_dir
        if short_folder_path:
            local_folder_path = path.join(local_dest_dir, sub('^/', '', 
                                                        short_folder_path))
            if not path.exists(local_folder_path):
                makedirs(local_folder_path)
        print 'LOCAL DIR\t', local_folder_path
        
        if len(folder_files) > 0:
            for folder_file in folder_files:
                remote_path = folder_path + '/' + folder_file
                print 'REMOTE FILE\t', remote_path  
                local_file_path = path.join(local_folder_path, folder_file)
                local_file_path = path.abspath(local_file_path)
                print 'LOCAL FILE\t', local_file_path  
                host.download_if_newer(remote_path, local_file_path)
        else:
            print 'NO FILES' 
    
        print ''

    host.close  
