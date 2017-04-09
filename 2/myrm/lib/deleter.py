import shutil
import os
import sys

# TODO separate filenames from paths


class Deleter(object):
    def __init__(self, options=dict()):
        self.options = options
        try:
            self.re_bin_location = self.options['re_bin_location']
        except KeyError:
            self.re_bin_location=os.path.join(os.environ['HOME'], 'recycle_bin')
            print 'using bin at {}'.format(self.re_bin_location)

        try:
            os.mkdir(self.re_bin_location)
        except OSError:
            print '{} already exists'.format(self.re_bin_location)
            sys.exit()

    def report_results(self, operation_results):
        if self.options['output'] is 'verbose' and len(operation_results) > 0:
            for i in operation_results:
                print i

    def deletedir(self, dirname):
        print 'dir'
        operation_results = []
        try:
            shutil.move(dirname, self.re_bin_location)
            operation_results.append('dir "{}" with all contents moved to {}'.format(dirname, self.re_bin_location))
        except OSError:
            if self.options['replace_same_name'] is True:
                shutil.rmtree(os.path.join(self.re_bin_location, dirname))
                shutil.copytree(dirname, self.re_bin_location)
                shutil.rmtree(dirname)
                operation_results.append('dir "{}" with all contents moved to {}'.format(dirname, self.re_bin_location))
            elif self.options['replace_same_name'] is False:
                print 'directory with name "{}" already exists in the recycle bin'.format(dirname)
        self.report_results(operation_results)
        return operation_results

    def deletefile(self, filename):
        operation_results = []
        try:
            shutil.move(filename, self.re_bin_location)
            operation_results.append('file "{}" moved to {}'.format(filename, self.re_bin_location))
        except OSError:
            if self.options['replace_same_name'] is True:
                shutil.copy2(filename, self.re_bin_location)
                os.remove(filename)
                operation_results.append('file "{}" moved to {}'.format(filename, self.re_bin_location))
            elif self.options['replace_same_name'] is False:
                print 'file with name "{}" already exists in {}\naborting'.format(filename, self.re_bin_location)
        self.report_results(operation_results)
        return operation_results

    def delete(self, object_name):  # wrapper that unites all delete methods and handles errors
        if os.path.exists(object_name):
            if os.path.isfile(object_name):
                self.deletefile(object_name)
            else:
                self.deletedir(object_name)
        else:
            print 'no file or dir named "{}"'.format(object_name)
            return
