import os


class Dryrunner(object):
    def __init__(self, files_to_delete_list, options):
        self.files_to_delete = []
        for i in files_to_delete_list:
            self.files_to_delete.append(os.path.split(i))
        self.dirlists = []
        self.dir_files = dict()
        for i in self.files_to_delete:
            if i[0] in self.dir_files.keys():
                self.dir_files[i[0]].append(i[1])
            else:
                self.dir_files[i[0]] = list(i[1])
        self.dir_files[os.getcwd()] = self.dir_files['']
        del(self.dir_files[''])

    def dryrun(self):
        for dirname in self.dir_files.keys():
            print "remaining contents of {}:".format(dirname)
            for fname in self.dir_files[dirname]:
                if fname not in os.listdir(dirname):
                    print "file named {} doesn't exist".format(os.path.join(dirname, fname))
            for filename in os.listdir(dirname):
                if filename not in self.dir_files[dirname]:
                    print filename
