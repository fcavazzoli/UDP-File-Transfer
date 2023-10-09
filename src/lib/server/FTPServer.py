import os
from lib.common.configs import SingletonConfiguration
from lib.common.file_handler import FileHandler

from lib.common.message import Message
from lib.constants import DEFAULT_MESSAGE_SIZE


class FTPServer():
    def __init__(self):
        self.file_name = None
        self.logger = SingletonConfiguration().get('logger')

    def handle_download(self, opt, payload, connection):
        file_name = payload.decode('utf-8')
        if not os.path.isfile('store/' + file_name):
            connection.send(Message.build_metadata_payload('ERROR_FILE_DOES_NOT_EXIST', 'download'))
            return
        else: 
            file_size = str(os.path.getsize('store/' + file_name))
            connection.send(Message.build_metadata_payload(file_size, 'download'))

        file_bytes = FileHandler('store/' + file_name).read_bytes(DEFAULT_MESSAGE_SIZE - 1)
        for msg in file_bytes:
            connection.send(Message.build_data_payload(msg))
        connection.send(Message.build_data_payload(b'exit'))
        connection.close()

    def handle_upload(self, opt, payload, connection):
        file_name = 'store/'+payload.decode('utf-8')
        if os.path.isfile(file_name):
            try:
                os.remove(file_name)
                self.logger.debug("The file '{0}' already exists. It has been deleted and started being replaced with the new one.".format(file_name))
            except OSError as e:
                self.logger.debug("Error deleting file '{0}': {1}".format(file_name, e))

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
        connection.close()
