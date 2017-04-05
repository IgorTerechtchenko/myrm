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
        operation_results = []
        try:
            try:
                shutil.move(dirname, self.re_bin_location + '/')
                operation_results.append('dir "{}" with all contents moved to {}'.format(dirname, self.re_bin_location))
            except shutil.Error:
                if self.options['replace_same_name'] is True:
                    shutil.rmtree(self.re_bin_location + '/' + dirname)
                    shutil.copytree(dirname, self.re_bin_location + '/' + dirname)
                    shutil.rmtree(dirname)
                    operation_results.append('dir "{}" with all contents moved to {}'.format(dirname, self.re_bin_location))
                elif self.options['replace_same_name'] is 'keep':
                    print 'directory with name "{}" already exists in the recycle bin'.format(dirname)
        except IOError:
            print 'no file dir "{}" located'.format(dirname)
        if self.options['output'] is 'verbose' and len(operation_results) > 0:
            for i in operation_results:
                print i
        return operation_results

    def deletefile(self, filename):
        operation_results = []
        try:
            try:
                shutil.move(filename, self.re_bin_location + '/')
                operation_results.append('file "{}" moved to {}'.format(filename, self.re_bin_location))
            except shutil.Error:
                if self.options['replace_same_name'] is True:
                    shutil.copy(filename, self.re_bin_location + '/')
                    os.remove(filename)
                    operation_results.append('file "{}" moved to {}'.format(filename, self.re_bin_location))
                elif self.options['replace_same_name'] is 'keep':
                    print 'file with name "{}" already exists in {}\naborting'.format(filename, self.re_bin_location)
        except IOError:
            print 'no file named "{}" located'.format(filename)
        if self.options['output'] is 'verbose' and len(operation_results) > 0:
            for i in operation_results:
                print i
        return operation_results


o = {'replace_same_name': True,
     'output': 'verbose'}
D = Deleter(options=o)
D.deletedir('dir')
D.deletefile('a')
D.deletefile('b')
