from queue import Queue


from ..Connection import Connection

class ConnectionsManagement:
    socket = None
    connections = {}
    
    def __init__(self, socket):
        self.socket = socket

    
    def new_message(self, clientAddress, message):
        if(not clientAddress in self.connections):
            self.connections[clientAddress] = Connection(str(len(self.connections)), clientAddress, message)
        else: 
            self.connections[clientAddress].received(message)

