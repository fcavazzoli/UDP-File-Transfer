import os
from lib.common.file_handler import FileHandler

from lib.common.message import Message
from lib.constants import DEFAULT_MESSAGE_SIZE


class FTPServer():
    def __init__(self):
        self.file_name = None

    def handle_download(self, opt, payload, connection):
        file_name = payload.decode('utf-8')
        print('el archivo existe', os.path.isfile('store/' + file_name))
        if not os.path.isfile('store/' + file_name):
            print('File does not exist')
            connection.send(Message.build_metadata_payload('ERROR_FILE_DOES_NOT_EXIST', 'download'))
            return

        file_bytes = FileHandler('store/' + file_name, None).read_bytes(DEFAULT_MESSAGE_SIZE - 1)
        for msg in file_bytes:
            connection.send(Message.build_data_payload(msg))
        connection.send(Message.build_data_payload(b'exit'))

    def handle_upload(self, opt, payload, connection):
        file_name = 'store/'+payload.decode('utf-8')
        print('file_name:', file_name)
        with open(file_name, 'ab') as f:
            while True:
                data = connection.recv()
                opt = Message.unwrap_operation_type(data)
                if opt == 'METADATA':
                    payload = Message.unwrap_payload_metadata(data)
                    if payload == b'ERROR_FILE_DOES_NOT_EXIST':
                        break
                payload = Message.unwrap_payload_data(data)
                if payload == b'exit':
                    break
                f.write(payload)
