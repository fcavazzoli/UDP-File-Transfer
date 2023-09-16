import socket

class Server:
    def __init__(self, udp_ip, port, logger):
        self.socket = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_DGRAM)
        self.socket.bind((udp_ip, port))
        self.logger = logger

    def serve(self):
        while True:
            data, addr = self.socket.recvfrom(1024)
            self.logger.info(f"New message from: {addr}")
            self.logger.info(f"Message:{data}")