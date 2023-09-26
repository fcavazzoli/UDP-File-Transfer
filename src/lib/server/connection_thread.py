from threading import Thread
from queue import Queue
import logging

from .connection import Connection


class ConnectionThread(Thread):
    """Thread class. It is in charge of managing a connection from a client."""

    queue = None

    def __init__(self, name, address):
        super().__init__()      # super calls the parent class constructor
        self.queue = Queue()
        self.name = name
        self.connection = Connection(address)

    def run(self):
        self.connection.send(bytes('Handshake Received %s' % self.name, "utf-8"))

        while (True):
            data, addrr = self.connection.recv()
            logging.info("Received this data: %s, from: %s", str(data), str(addrr))
            response = bytes('OK Received for thread %s' % self.name, "utf-8")
            self.connection.send(response)
            if (data == b'exit'):
                break

        self.connection.send(bytes('EXIT Received %s' % self.name, "utf-8"))
