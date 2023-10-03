from lib.common.socket import Socket
from lib.common.configs import SingletonConfiguration
from lib.server.threads_manager import ThreadsManager


class Server:
    def __init__(self, ip, port):
        self.socket = Socket.bind(ip, port)
        self.logger = SingletonConfiguration().get('logger')
        self.threads_manager = ThreadsManager()
        self.logger.info("Server started at %s:%s" % (ip, port))

    def serve(self):
        while True:
            data, addr = self.socket.recv()
            self.logger.info("Received new connection from: {0}".format(addr))
            handshake = bytes(data).decode('utf-8').split(' ')
            if (handshake[0] != 'handshake'):
                raise Exception('Invalid handshake')
            self.threads_manager.new_connection(addr)

    # def close(self):
    #     self.threads_manager.close()
    #     self.socket.close()
