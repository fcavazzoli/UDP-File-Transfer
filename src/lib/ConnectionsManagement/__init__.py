from queue import Queue


from ..Connection import Connection


class ConnectionsManagement:
    socket = None
    connections = {}

    def __init__(self, socket):
        self.socket = socket

    def new_message(self, address, port, message):
        if (not (address, port) in self.connections):
            self.connections[(address, port)] = Connection(str(len(self.connections)), address, message)
        else:
            self.connections[(address, port)].received(message)
