import shutil
import os
import json
import random


class Deleter(object):
    def __init__(self, options=dict()):
        #  TODO process unexisting rebin location
        self.options = options
        try:
            self.re_bin_location = self.options['re_bin_location']
        except KeyError:
            self.re_bin_location=os.path.join(os.environ['HOME'], 'recycle_bin')
            print 'using {}'.format(self.re_bin_location)

        try:
            os.mkdir(os.path.join(self.re_bin_location, 'info'))
            os.mkdir(os.path.join(self.re_bin_location, 'trash'))
        except OSError:
            print 'using {}'.format(self.re_bin_location)

        self.trash_location = os.path.join(self.re_bin_location, 'trash')
        self.info_location = os.path.join(self.re_bin_location, 'info')
        self.info_file_location = os.path.join(self.info_location, 'info_file')

    def add_record(self, object_name):
        f = open(self.info_file_location, 'a')
        object_full_name = os.path.abspath(object_name)
        object_id = object_name + str(random.random())
        print object_id
        f.writelines('{}; {} \n'.format(object_full_name, object_id))
        f.close()

    def create_file_proxy(self, filename): #  TODO doesn't work
        info_name = os.path.join(self.info_location, str(os.path.split(os.path.abspath(filename))[0]))
        direrctory = os.path.split(os.path.abspath(filename))[0]
        info_name = self.info_location + direrctory
        print info_name
        try:
            os.makedirs(info_name)
        except OSError:
            pass
        shutil.copy2(filename, os.path.join(info_name, filename))


    def report_results(self, operation_results):
        try:
            if self.options['output'] is 'verbose' and len(operation_results) > 0:
                for i in operation_results:
                    print i
        except KeyError:
            return

    def deletedir(self, dirname):
        operation_results = []
        try:
            shutil.move(dirname, self.trash_location)
            operation_results.append('dir "{}" with all contents moved to {}'.format(dirname, self.re_bin_location))
        except shutil.Error:
            if self.options['replace_same_name'] is True:
                try:
                    shutil.rmtree(os.path.join(self.trash_location, dirname))
                except OSError:
                    os.remove(os.path.join(self.trash_location, dirname))
                shutil.move(dirname, self.trash_location)
                operation_results.append('dir "{}" with all contents moved to {}'.format(dirname, self.re_bin_location))
            elif self.options['replace_same_name'] is False:
                print 'directory with name "{}" already exists in the recycle bin'.format(dirname)
        self.report_results(operation_results)
        return operation_results

    def deletefile(self, filename):
        operation_results = []
        self.create_file_proxy(filename)
        try:
            shutil.move(filename, self.trash_location)
            operation_results.append('file "{}" moved to {}'.format(filename, self.re_bin_location))
        except shutil.Error:
            if self.options['replace_same_name'] is True:
                try:
                    shutil.copy2(filename, self.trash_location)
                    os.remove(filename)
                except IOError:
                    shutil.rmtree(os.path.join(self.trash_location, filename))
                    shutil.move(filename, self.trash_location)
                operation_results.append('file "{}" moved to {}'.format(filename, self.re_bin_location))
            elif self.options['replace_same_name'] is False:
                print 'file with name "{}" already exists in {}\naborting'.format(filename, self.re_bin_location)
        self.report_results(operation_results)
        return operation_results

    def delete(self, object_name):  # wrapper that unites all delete methods and handles errors
        try:
            if self.options['output'] == 'verbose':
                print 'deleting {}'.format(object_name)
        except KeyError:
            pass
        if os.path.exists(object_name):
            if os.path.isfile(object_name):
                print 'file'
                self.deletefile(object_name)
            elif os.path.isdir(object_name):
                print 'dir'
                self.deletedir(object_name)
            self.add_record(object_name)
        else:
            print 'no file or dir named "{}"'.format(object_name)
        return
