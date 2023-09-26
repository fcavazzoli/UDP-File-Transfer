import socket

from .threads_manager import ThreadsManger


class Server:
    """Server class. It is in charge of listening to incoming connections and
    managing them."""
    def __init__(self, udp_ip, port, logger):
        self.socket = socket.socket(socket.AF_INET,  # AF_INET = IPv4
                                    socket.SOCK_DGRAM)      # SOCK_DGRAM = UDP
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
