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
        while True:
            data = self.connection.recv()
            opt = Message.unwrap_operation_type(data)
            payload = Message.unwrap_payload_data(data)
            print('OPT: ', opt)
            if opt == 'METADATA':
                if Message.unwrap_action_type(data) == 0: # 0 = download
                    print('SERVER received download message')
                    ftp_server.handle_download(opt, payload, self.connection)
            if payload == b'exit':
                print('SERVER received exit message')
            ftp_server.handle_new_message(opt, payload)
            print('SERVER received message: {0}\n - payload:{1},'.format(opt, payload))
           
