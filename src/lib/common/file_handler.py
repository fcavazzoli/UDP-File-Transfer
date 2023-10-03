import logging

from lib.common.configs import SingletonConfiguration


class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.logger = SingletonConfiguration().get('logger')

    def read_bytes(self, chunk_size):
        try:
            with open(self.file_path, 'rb') as file:
                messages = []
                if chunk_size is None:
                    file_bytes = file.read()
                else:
                    while True:
                        chunk = file.read(chunk_size)
                        if not chunk:
                            break
                        messages.append(chunk)
                return messages
        except FileNotFoundError:
            self.logger.error('File {0} not found'.format(self.file_path))
            return None
        except PermissionError:
            self.logger.error('Permission denied for file {0}'.format(self.file_path))
            return None

    def write_bytes(self, file_bytes):
        try:
            with open(self.file_path, 'ab') as file:
                file.write(file_bytes)
        except FileNotFoundError:
            self.logger.error('File {0} not found'.format(self.file_path))
            return None
        except PermissionError:
            self.logger.error('Permission denied for file {0}'.format(self.file_path))
            return None
