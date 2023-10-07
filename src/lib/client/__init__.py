from lib.common.connection import Connection
from lib.common.configs import SingletonConfiguration


class Client:
    def __init__(self, remote_ip, remote_port):
        self.connection = Connection()
        self.address = (remote_ip, remote_port)
        self.logger = SingletonConfiguration().get('logger')

    def connect(self):
        self.connection.connect(self.address)
        self.logger.info('Connected to server')
  
    def send(self, message):
        self.connection.send(message)

    def recv(self):
        return self.connection.recv()
    
    def messages_on_window(self):
        return self.connection.messages_on_window()
    
    def close(self):
        self.connection.close()
        self.logger.info('Connection closed')
