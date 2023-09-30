from ..common.socket import Socket
from .threads_manager import ThreadsManager


class Server:
    def __init__(self, ip, port, logger):
        self.socket = Socket.bind(ip, port)
        self.logger = logger
        self.threads_manager = ThreadsManager()
        print("Server started at %s:%s" % (ip, port))

    def serve(self):
        while True:
            data, addr = self.socket.recv()
            print("received new connection: %s" % data)
            handshake = bytes(data).decode('utf-8').split(' ')
            if (handshake[0] != 'handshake'):
                raise Exception('Invalid handshake')
            self.threads_manager.new_connection(addr)
