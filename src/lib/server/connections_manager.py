from .connection import Connection


class ConnectionsManager:
    socket = None
    connections = {}

    def __init__(self, socket):
        self.socket = socket

    def new_message(self, clientAddress, message):
        if (clientAddress not in self.connections):
            self.connections[clientAddress] = Connection(str(len(self.connections)), clientAddress, message)
        else:
            self.connections[clientAddress].received(message)
