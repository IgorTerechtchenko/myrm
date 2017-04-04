#!/usr/bin/env python

import shutil
import os


class Deleter(object):
    def __init__(self, re_bin_location=os.environ['HOME'] + '/recycle_bin',
                 options=dict()):
        self.re_bin_location = re_bin_location
        try:
            os.mkdir(self.re_bin_location)
        except OSError:
            'using bin at {}'.format(re_bin_location)
        self.options = options

    def deletedir(self, dirname):
        if dirname in os.listdir(self.re_bin_location):
            if self.options['same_name_confres'] is 'replace':
                shutil.copytree(dirname, self.re_bin_location + '/')
                shutil.rmtree(dirname)
            elif self.options['same_name_confres'] is 'keep':
                print 'file with such name already exists in the recycle bin'
        else:
            shutil.move(dirname, self.re_bin_location + '/')

    def deletefile(self, filename):
        if filename in os.listdir(self.re_bin_location):
            if self.options['same_name_confres'] is 'replace':
                shutil.copy(filename, self.re_bin_location + '/')
                os.remove(filename)
            elif self.options['same_name_confres'] is 'keep':
                print 'file with name "{}" already exists in the recycle bin'.format(filename)
        else:
            shutil.move(filename, self.re_bin_location + '/')


o = {'same_name_confres': 'keep'}
D = Deleter(options=o)
D.deletefile('a')
