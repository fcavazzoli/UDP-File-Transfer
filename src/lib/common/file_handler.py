import logging

from lib.common.message import Message


class FileHandler:
    def __init__(self, file_path, logger: logging.Logger):
        self.file_path = file_path
        self.logger = logger

    def read_bytes(self, chunk_size):
        try:
            with open(self.file_path, 'rb') as file:
                seq_num = 0
                messages = []
                print(f'chunk_size: {chunk_size}')
                if chunk_size is None:
                    file_bytes = file.read()
                else:
                    while True:
                        chunk = file.read(chunk_size)
                        if not chunk:
                            break
                        message = Message().set_header(seq_num).set_payload(chunk).build()
                        messages.append(message)
                        seq_num += 1
                return messages
        except FileNotFoundError:
            self.logger.error(f'File {self.file_path} not found')
            return None
        except PermissionError:
            self.logger.error(f'Permission denied for file {self.file_path}')
            return None

    def write_bytes(self, file_bytes):
        try:
            with open(self.file_path, 'wb') as file:
                file.write(file_bytes)
        except FileNotFoundError:
            self.logger.error(f'File {self.file_path} not found')
            return None
        except PermissionError:
            self.logger.error(f'Permission denied for file {self.file_path}')
            return None
