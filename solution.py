class FileReader:

    def __init__(self, path):
        self.path = path

    def read(self):
        try:
            f = open(self.path, 'r')
            ret = f.read()
            f.close()
            return ret

        except IOError:
            return ""



