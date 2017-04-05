#!/usr/bin/env python

import shutil
import os

# TODO separate filenames from paths


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
        try:
            shutil.move(dirname, self.re_bin_location + '/')
        except shutil.Error:
            if self.options['same_name_confres'] is 'replace':
                shutil.rmtree(self.re_bin_location + '/' + dirname)
                shutil.copytree(dirname, self.re_bin_location + '/' + dirname)
                shutil.rmtree(dirname)
            elif self.options['same_name_confres'] is 'keep':
                print 'directory with name "{}" already exists in the recycle bin'.format(dirname)

    def deletefile(self, filename):
        operation_results = []
        try:
            try:
                shutil.move(filename, self.re_bin_location + '/')
                operation_results.append('file {} moved to {}'.format(filename, self.re_bin_location))
            except shutil.Error:
                if self.options['same_name_confres'] is 'replace':
                    shutil.copy(filename, self.re_bin_location + '/')
                    os.remove(filename)
                    operation_results.append('file {} moved to {}'.format(filename, self.re_bin_location))
                elif self.options['same_name_confres'] is 'keep':
                    print 'file with name "{}" already exists in {}\naborting'.format(filename, self.re_bin_location)
        except IOError:
            print 'no file named "{}" located'.format(filename)
        if self.options['output'] is 'verbose' and len(operation_results) > 0:
            for i in operation_results:
                print i


o = {'same_name_confres': 'replace',
     'output': 'verbose'}
D = Deleter(options=o)
D.deletedir('dir')
