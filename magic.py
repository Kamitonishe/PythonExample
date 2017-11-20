import os
import tempfile

class File:

    def __init__(self, path):
        self.path = path
        f = open(path, 'w')
        f.close()


    def write(self, text):
        with open(self.path, 'w') as f:
            f.write(text)

    def __add__(self, other):
        self_dir_name, self_file_name = os.path.split(self.path)
        other_dir_name, other_file_name = os.path.split(other.path)
        path = os.path.join(tempfile.gettempdir(), self_file_name + other_file_name)



        with open(path, 'a') as af:
            with open(self.path, 'r') as rf:
                af.write(rf.read())
            with open(other.path, 'r') as rf:
                af.write(rf.read())

        return File(path)

    def __iter__(self):
        self.read_file = open(self.path, 'r')
        return self

    def __next__(self):
        line = self.read_file.readline()

        if line == '':
            self.read_file.close()
            raise StopIteration

        return line


    def __str__(self):
        return self.path
