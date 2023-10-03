from lib.common.connection import Connection


class Client:
    def __init__(self, remote_ip, remote_port, logger):
        self.connection = Connection()
        self.address = (remote_ip, remote_port)
        self.logger = logger

    def connect(self):
        self.connection.connect(self.address)
        self.logger.info('Connected to server')

    def send(self, message):
        self.connection.send(message)

    def recv(self):
        return self.connection.recv()
