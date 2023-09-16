import socket

class Client:
    def __init__(self, remote_ip, remote_port, logger):
        self.socket = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_DGRAM)
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.logger = logger

    def send(self, message):
        print("UDP target IP: %s" % self.remote_ip)
        print("UDP target port: %s" % self.remote_port)
        print("message: %s" % message)
        self.socket.sendto(message, (self.remote_ip, self.remote_port))
