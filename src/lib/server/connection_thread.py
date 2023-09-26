from threading import Thread
from queue import Queue

from .connection import Connection


class ConnectionThread(Thread):

    queue = None

    def __init__(self, name, address):
        super(ConnectionThread, self).__init__()
        self.queue = Queue
        self.name = name
        self.connection = Connection(address)

    def run(self):
        self.connection.send(bytes('Handshake Received %s' % self.name, "utf-8"))
        self.connection.listen()
        while True:
            data = self.connection.recv()
            print('SERVER received message: %s' % data)    

