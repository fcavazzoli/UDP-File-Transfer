from threading import Thread
from queue import Queue
import logging

from lib.common.message import Message
from lib.server.FTPServer import FTPServer

from lib.common.connection import Connection


class ConnectionThread(Thread):
    """Thread class. It is in charge of managing a connection from a client."""

    queue = None

    def __init__(self, name, address):
        super(ConnectionThread, self).__init__()
        self.queue = Queue
        self.name = name
        self.address = address
        self.connection = Connection()

    def run(self):
        self.connection.accept(self.address)
        ftp_server = FTPServer()
        data = self.connection.recv()
        opt = Message.unwrap_operation_type(data)
        if opt == 'METADATA':
            payload = Message.unwrap_payload_metadata(data)
            if Message.unwrap_action_type(data) == 0:  # 0 = download
                ftp_server.handle_download(opt, payload, self.connection)
            elif Message.unwrap_action_type(data) == 1:  # 1 = upload
                ftp_server.handle_upload(opt, payload, self.connection)

    # def close(self):
    #     self.connection.close()
