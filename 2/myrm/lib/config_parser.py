import json


class ConfigParser(object):
    def __init__(self, config_file_path):
        try:
            f = open(config_file_path, 'r')
        except IOError:
            print 'no file named "{}"'.format(config_file_path)
        self.options_dict = json.loads(f.read())
        print self.options_dict


cp = ConfigParser('config')
