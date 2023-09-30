import logging

class FileHandler:
    def __init__(self, file_path, logger: logging.Logger):
        self.file_path = file_path
        self.logger = logger

    def read_bytes(self, chunk_size=None):
        try:
            with open(self.file_path, 'rb') as file:
                if chunk_size is None:
                    file_bytes = file.read()
                else:
                    file_bytes = bytearray()
                    while True:
                        chunk = file.read(chunk_size)
                        if not chunk:
                            break
                        file_bytes.extend(chunk)

                return file_bytes
        except FileNotFoundError:
            self.logger.error(f'File {self.file_path} not found')
            return None
        except PermissionError:
            self.logger.error(f'Permission denied for file {self.file_path}')
            return None

