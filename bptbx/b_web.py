r"""This module contains tools for web connectivity etc."""

from os import path, makedirs
from re import sub
from ftputil import FTPHost
from bptbx import b_legacy
import re
from bs4 import BeautifulSoup
urllib2 = b_legacy.b_urllib2()
import re
from bs4 import BeautifulSoup

DEFAULT_USER_AGENT = ('Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127' +
                      ' Firefox/2.0.0.11')
DEFAULT_ACCEPT = 'text/html'


def download_webpage_to_list(webpage_url, *header_tupels):
    """Downloads a webpage and writes content into a line-by-line list."""

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

    if found_ext_useragent == False:
        headers.append(('User-Agent', DEFAULT_USER_AGENT))
    if found_ext_accept == False:
        headers.append(('Accept', DEFAULT_ACCEPT))

    opener.addheaders = headers
    input_file_handle = opener.open(webpage_url)
    webpage_url = input_file_handle.readlines()
    input_file_handle.close()
    return webpage_url


def download_file(file_url, target_filepath):
    """Downloads a file url to a given target filepath."""
    remote_file = urllib2.urlopen(file_url)
    output = open(target_filepath, 'wb')
    output.write(remote_file.read())
    output.close()


def recursively_download_ftp(host, username, password, ftp_root_path,
                             local_dest_dir):

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
            local_folder_path = path.join(local_dest_dir, sub('^/', '',
                                                              short_folder_path))
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


def extract_main_text_content(html):
    """A method to extract the main content of a given HTML page. This code
    has been adapted from http://nirmalpatel.com/fcgi/hn.py (GPLv3) written
    by Nirmal Patel."""

    negative = re.compile('comment|meta|footer|footnote|foot')
    positive = re.compile('post|hentry|entry|content|text|body|article')
    punctation = re.compile('''[!'#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]''')

    replace_brs = re.compile('<br */? *>[ \r\n]*<br */? *>')
    html = re.sub(replace_brs, '</p><p>', html)

    try:
        soup = BeautifulSoup(html, 'html.parser')
    except:
        return ''

    # REMOVE SCRIPTS
    for s in soup.findAll('script'):
        s.extract()

    all_paragraphs = soup.findAll('p')
    top_parent = None

    parents = []
    for paragraph in all_paragraphs:

        parent = paragraph.parent

        if (parent not in parents):
            parents.append(parent)
            parent.score = 0

            if (parent.has_attr('class')):
                if (negative.match(str(parent['class']))):
                    parent.score -= 50
                if (positive.match(str(parent['class']))):
                    parent.score += 25

            if (parent.has_attr('id')):
                if (negative.match(str(parent['id']))):
                    parent.score -= 50
                if (positive.match(str(parent['id']))):
                    parent.score += 25

        if (parent.score == None):
            parent.score = 0

        # ''.join(paragraph.findAll(text=True))
        inner_text = paragraph.renderContents()
        if (len(inner_text) > 10):
            parent.score += 1

        parent.score += str(inner_text).count(',')

    for parent in parents:
        if ((not top_parent) or (parent.score > top_parent.score)):
            top_parent = parent

    if (not top_parent):
        return ''

    # REMOVE LINK'D STYLES
    style_links = soup.findAll('link', attrs={'type': 'text/css'})
    for s in style_links:
        s.extract()

    # REMOVE ON PAGE STYLES
    for s in soup.findAll('style'):
        s.extract()

    # CLEAN STYLES FROM ELEMENTS IN TOP PARENT
    for ele in top_parent.findAll(True):
        del(ele['style'])
        del(ele['class'])

    _extract_main_text_content_remove_divs(top_parent)
    _extract_main_text_content_clean(top_parent, 'form')
    _extract_main_text_content_clean(top_parent, 'object')
    _extract_main_text_content_clean(top_parent, 'iframe')

    full_text = top_parent.renderContents().decode('utf-8')
    full_text_final = []
    for line in full_text.split('\n'):
        if not line.strip():
            continue
        line = re.sub('<[^>]+>', '', line).strip()
        if line:
            full_text_final.append(line)
    return '\n'.join(full_text_final)


def _extract_main_text_content_clean(top, tag, min_words=10000):
    tags = top.findAll(tag)
    for t in tags:
        if (str(t.renderContents()).count(' ') < min_words):
            t.extract()


def _extract_main_text_content_remove_divs(parent):
    divs = parent.findAll('div')
    for d in divs:
        p = len(d.findAll('p'))
        img = len(d.findAll('img'))
        li = len(d.findAll('li'))
        a = len(d.findAll('a'))
        embed = len(d.findAll('embed'))
        pre = len(d.findAll('pre'))
        code = len(d.findAll('code'))

        if (str(d.renderContents()).count(',') < 10):
            if ((pre == 0) and (code == 0)):
                if ((img > p) or (li > p) or (a > p) or (p == 0) or (embed > 0)):
                    d.extract()

if __name__ == '__main__':
    import requests
    import sys
    if len(sys.argv) < 2:
        print('You must provide a valid URL.')
        exit(1)
    r = requests.get(sys.argv[1], timeout=5)
    main_text = extract_main_text_content(r.text)
    print(main_text)
