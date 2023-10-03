import os
from lib.FileNotFoundException import FileNotFoundException


class File:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.file = None

    def isFile(self):
        if not os.path.isfile(self.path):
            raise FileNotFoundException()

    def size(self):
        return os.path.getsize(self.path)

    def open(self, mode):
        """
        Opens the file in the given mode and saves it in the 'file' attribute value.

        e.g.: "mode" parameter 'rb', 'b', 'wb', 'w', etc.
        """
        self.file = open(self.path + '/' + self.name, mode)

    def write(self, data):
        self.file.write(data)

    def read(self, size):
        return self.file.read(size)

    def close(self):
        self.file.close()
