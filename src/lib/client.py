import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

class Client:
    def __init__(self, remote_ip, remote_port, logger):
        self.socket = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_DGRAM)
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.logger = logger
        self.socket.bind((UDP_IP, 0))
        self.listening_port = self.socket.getsockname()[1]

    def _send(self, message):
        self.socket.sendto(message, (self.remote_ip, self.remote_port))

    def _receive(self):
        return self.socket.recvfrom(1024)

    def connect(self):
        self._send(bytes('handshake %s' % self.listening_port, "utf-8"))
        data, addr = self._receive()
        print("handshake response: %s" % data)

    def send(self, message):
        self._send(message)
        data, addr = self._receive()
        print("response: %s" % data)

