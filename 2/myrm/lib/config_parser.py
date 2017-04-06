import json
import sys


class ConfigParser(object):
    def __init__(self, config_file_path):
        try:
            f = open(config_file_path, 'r')
            self.options_dict = json.loads(f.read())
        except IOError:
            print 'no file named "{}"'.format(config_file_path)

    def get_options(self):
        try:
            return self.options_dict
        except NameError:
            print 'no optoins parsed'
            sys.exit()
