import socket

# UDP_IP = "127.0.0.1"
# UDP_PORT = 5005


class Client:
    def __init__(self, remote_ip, remote_port, logger):
        self.socket = socket.socket(socket.AF_INET,    # AF_INET = IPv4
                                    socket.SOCK_DGRAM)  # SOCK_DGRAM = UDP
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.logger = logger

    def _send(self, message):
        self.socket.sendto(message, (self.remote_ip, self.remote_port))

    def _receive(self):
        return self.socket.recvfrom(1024)

    def connect(self):
        self._send(bytes('handshake', "utf-8"))
        data, addr = self._receive()
        print("handshake response: %s" % data)
        self.remote_address = addr[0]
        self.remote_port = addr[1]

    def send(self, message):
        self._send(message)
        data, addr = self._receive()
        print("response: %s" % data)
