import socket

class Client:
    def __init__(self, remote_ip, remote_port, logger):
        self.socket = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_DGRAM)
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.logger = logger

    def send(self, message):
        self.logger.info(f"UDP target IP: {self.remote_ip}, UDP target port: {self.remote_port}")
        self.logger.info(f"message:{message}")
        self.socket.sendto(message, (self.remote_ip, self.remote_port))
