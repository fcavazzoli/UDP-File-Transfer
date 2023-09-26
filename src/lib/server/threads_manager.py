from .connection_thread import ConnectionThread


class ThreadsManager:
    connections = {}

    def __init__(self):
        pass

    def new_connection(self, clientAddress):
        if (clientAddress not in self.connections):
            # el nombre del thread es el numero de conexion
            self.connections[clientAddress] = ConnectionThread(str(len(self.connections)), clientAddress)
            self.connections[clientAddress].start()