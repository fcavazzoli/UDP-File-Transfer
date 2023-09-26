from socket import socket

from .connection_thread import ConnectionThread


class Connection:
    address = None
    socket = None

    def __init__(self, address):
        self.address
        self.socket = socket.socket(socket.AF_INET,    # AF_INET = IPv4
                                    socket.SOCK_DGRAM)  # SOCK_DGRAM = UDP
        
    def send(self, message):
        self.socket.sendto(message, address)

    def recv(self):
        return self.socket.recvfrom(1024)
        
    
