#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" outliers is helper to identify files which have been created in isolated time window """

# author : Hrvoje Spoljar
# email  : hrvoje.spoljar@gmail.com

import os
import sys

# TODO :
# - filter extensions
# - ctime filter to avoid searching files older than X

TIME_DIFF = 3

def file_list(path):
    """ returns list of files in path and sub directories as list of dictionaries
        e.g.
        [ {'ctime' : 1461953797, 'file' : ./foo}, {'ctime' : 1461953832, 'file' : ./bar}]
    """

    elements = []
    for dirname, dirnames, filenames in os.walk(path):

        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        if '.git' in dirnames:
            # don't go into any .git directories.
            dirnames.remove('.git')

        # print path to all filenames
        for filename in filenames:
            file_path = os.path.join(dirname, filename)
            ctime = os.stat(file_path).st_ctime

            item = {'ctime' : ctime, 'file' : file_path}
            elements.append(item)

    sorted_list = sorted(elements, key=lambda k: k['ctime'])
    return sorted_list


def main(path):
    """ main func, compares ctimes of adjecent files in ordered time list
        to identify outliers created in isolated time window
    """

    sorted_list = file_list(path)
    for index in xrange(0, len(sorted_list)-1):
        if index == 0:
            continue
        prev_item = sorted_list[index-1]
        next_item = sorted_list[index+1]
        item = sorted_list[index]

        if prev_item['ctime'] + TIME_DIFF < item['ctime'] and \
           item['ctime'] + TIME_DIFF < next_item['ctime']:
            print item['file']


if __name__ == '__main__':
    try:
        SEARCH_PATH = sys.argv[1]
    except IndexError:
        SEARCH_PATH = '.'

    if os.path.isdir(SEARCH_PATH):
        sys.stderr.write("SEARCHING PATH : %s \n" %(SEARCH_PATH))
    else:
        print "Can't find specified directory"
        sys.exit(1)
    main(SEARCH_PATH)
