from threading import Thread
from queue import Queue
import logging

from lib.common.message import Message

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
        while True:
            data = self.connection.recv()
            opt = Message.unwrap_operation_type(data)
            payload = Message.unwrap_payload_data(data)
            # opt tiene el tipo de operacion (METADATA o DATA)
            # el payload de un mensaje METADATA es el nombre del archivo
            # el payload de un mensaje DATA es un conjunto de bytes del contenido del archivo
            print('SERVER received message: {0}\n - payload:{1},'.format(opt, payload))
           
