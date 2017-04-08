import shutil
import os

# TODO separate filenames from paths


class Deleter(object):
    def __init__(self, re_bin_location=os.path.append(os.environ['HOME'], '/recycle_bin'),
                 options=dict()):
        self.re_bin_location = re_bin_location
        try:
            os.mkdir(self.re_bin_location)
        except OSError:
            'using bin at {}'.format(re_bin_location)
        self.options = options

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
        except shutil.Error:
            if self.options['replace_same_name'] is True:
                shutil.rmtree(self.re_bin_location + '/' + dirname)
                shutil.copytree(dirname, os.path.join(self.re_bin_location, dirname))
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
        except shutil.Error:
            if self.options['replace_same_name'] is True:
                shutil.copy(os.path.join(filename, self.re_bin_location))
                os.remove(filename)
                operation_results.append('file "{}" moved to {}'.format(filename, self.re_bin_location))
            elif self.options['replace_same_name'] is False:
                print 'file with name "{}" already exists in {}\naborting'.format(filename, self.re_bin_location)
        self.report_results(operation_results)
        return operation_results

    def delete(self, object_name):  # wrapper that unites all delete methods and handles errors
        try:
            if os.path.isfile(object_name):
                self.deletefile(object_name)
            else:
                self.deletedir(object_name)
        except OSError:
            print 'no file or directory named "{}"'.format(object_name)
