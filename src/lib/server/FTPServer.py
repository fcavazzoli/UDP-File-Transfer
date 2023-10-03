import os
from lib.common.file_handler import FileHandler

from lib.common.message import Message
from lib.constants import DEFAULT_MESSAGE_SIZE


class FTPServer():
    def __init__(self):
        self.file_name = None
        

    def handle_new_message(self, opt, payload):
        if opt == 'METADATA':
            self.handle_metadata(payload)
        elif opt == 'DATA':
            self.handle_data(payload)
        else:
            print(f'Unknown operation type {opt}')

    def handle_metadata(self, payload: bytes):
        file_name = payload.decode('utf-8')
        self.file_name = 'store/' + file_name
    
    def handle_data(self, payload: bytes):
        with open(self.file_name, 'ab') as f:
            f.write(payload)

    def handle_download(self, opt, payload, connection):
        file_name = payload.decode('utf-8')
        print('el archivo existe', os.path.isfile('store/' + file_name))
        if not os.path.isfile('store/' + file_name):
            print('File does not exist')
            connection.send(Message.build_metadata_payload('ERROR_FILE_DOES_NOT_EXIST', 'download'))
            return

        file_bytes = FileHandler('store/' + file_name, None).read_bytes(DEFAULT_MESSAGE_SIZE-1)
        for msg in file_bytes:
            connection.send(Message.build_data_payload(msg))


