#!/usr/bin/env python

import sys
import os
import argparse
import re
import shutil
all = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(all)

from lib import deleter
from lib import config_parser

parser = argparse.ArgumentParser()
parser.add_argument('-remove', nargs='*', help='files to delete')
parser.add_argument('-show', help='show last SHOW contents of recycle bin', type=int)
parser.add_argument('-re', help='delete all files/dirs matching RE', type=str)
parser.add_argument('-clear', help='clear da bin', action='store_true')


def show_re_bin(re_bin_location, num):
    print 'contents of recycle bin at "{}"'.format(re_bin_location)
    for i in os.listdir(re_bin_location)[-num:]:
        print i


def process_files_re(exp, deleter):
    files_to_delete = []
    found = False
    try:
        expression = re.compile(exp)
    except re.error:
        print "Invalid regexp"
        return
    for i in os.listdir(os.curdir):
        result = expression.match(i)
        if result is not None:
            files_to_delete.append(i)
            found = True
    if found is not True:
        print "No matches found."
        return
    for i in files_to_delete:
        deleter.delete(i)


def clear_re_bin(re_bin_location):
    for i in os.listdir(re_bin_location):
        location = os.path.join(re_bin_location, i)
        try:
            shutil.rmtree(location)
        except OSError:
            os.remove(location)
        print '{} removed'.format(i)


def main():
    C = config_parser.ConfigParser('/home/pokapoka/coded/python/ISP/take2/2/myrm/bin/config')
    options = C.get_options()
    re_bin_location = options['re_bin_location']

    args = parser.parse_args()

    D = deleter.Deleter(options)

    if options['automatic_clear_policy'] and len(os.listdir(re_bin_location)) > 5:
        clear_re_bin(re_bin_location)

    if args.remove:
        for i in args.remove:
            D.delete(i)
    if args.show:
        show_re_bin(re_bin_location, args.show)
        sys.exit()
    if args.re:
        process_files_re(args.re, D)
        sys.exit()
    if args.clear:
        clear_re_bin(re_bin_location)
        sys.exit()

if __name__ == '__main__':
    main()
