import socket

from .threads_manager import ThreadsManger


class Server:
    def __init__(self, udp_ip, port, logger):
        self.socket = socket.socket(socket.AF_INET,  # Internet
                                    socket.SOCK_DGRAM)
        self.socket.bind((udp_ip, port))
        self.logger = logger
        self.threads_manager = ThreadsManager()

    def serve(self):
        while True:
            data, addr = self.socket.recvfrom(1024)
            print("received new connection: %s" % data)
            handshake = bytes(data).decode('utf-8').split(' ')
            if (handshake[0] != 'handshake'):
                raise Exception('Invalid handshake')
            self.threads_manager.new_connection(addr)
