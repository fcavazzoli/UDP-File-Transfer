from threading import Thread
from queue import Queue

from .connection import Connection


class ConnectionThread(Thread):

    queue = None

    def __init__(self, name, address):
        super().__init__()      # super calls the parent class constructor
        self.queue = Queue()
        self.name = name
        self.connection = Connection(address)

    def run(self):
        self.connection.send(bytes('Handshake Received %s' % self.name, "utf-8"))

        while (True):
            data = self.connection.recv()
            response = bytes('OK Received %s' % self.name, "utf-8")
            self.connection.send(response)
            if (data == b'exit'):
                break

        self.connection.send(bytes('EXIT Received %s' % self.name, "utf-8"))
