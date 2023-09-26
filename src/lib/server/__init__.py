import socket

from .threads_manager import ThreadsManager


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
            # waits for a new connection. When a new connection is received, it creates a new thread
            data, addr = self.socket.recvfrom(1024)         # number of bytes to be read from UDP socket
            self.logger.info("Received new connection from %s" % str(addr))
            handshake = bytes(data).decode('utf-8').split(' ')
            if (handshake[0] != 'handshake'):
                raise Exception('Invalid handshake')
            self.threads_manager.new_connection(addr)
            
        
