import socket 
from lib.constants import DEFAULT_PORT, DEFAULT_IP_ADDR

# Buffer size of 1472 bytes for UDP sockets, 
# is the maximum payload size allowed within a single Ethernet 
# frame without fragmentation.
# 1500 (max size) - 28 (additional data) = 1472 bytes
BUFFER_SIZE = 1472

class CustomSocket:
    def __init__(self, ipAddr = None, port = None):
        self.ipAddr = ipAddr or DEFAULT_IP_ADDR
        self.port = port or DEFAULT_PORT

        # AF_INET: IPv4 - SOCK_DGRAM: UDP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.buffer = BUFFER_SIZE

    # Bind's the socket to an specific ip and port
    def bind(self):
        self.socket.bind((self.ipAddr, self.port))

    def receive(self):
        msg, ip = self.socket.recvfrom(self.buffer)
        return msg, ip
    
    def send(self, data):
        address = self.ipAddr, self.port
        self.socket.sendto(data, address)

    def sendTo(self, data, address):
        self.socket.sendto(data, address)

    def close(self):
        self.socket.close()