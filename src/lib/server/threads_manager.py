from .connection_thread import ConnectionThread


class ThreadsManager:
    # connections = {}

    def __init__(self):
        self.connections = {}

    def new_connection(self, clientAddress):
        # el nombre del thread es el numero de conexion
        self.connections[clientAddress] = ConnectionThread(str(len(self.connections)), clientAddress)
        self.connections[clientAddress].start()     # start is a method of Thread class

    def close(self):
        for connection in self.connections.values():
            connection.close()
            connection.join()
