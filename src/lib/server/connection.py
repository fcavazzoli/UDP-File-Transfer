from socket import socket

from .connection_thread import ConnectionThread


class Connection:
    address = None
    socket = None

    def __init__(self, address):
        self.address
        self.socket = socket.socket(socket.AF_INET,  # Internet
                                    socket.SOCK_DGRAM)
        
    def send(self, message):
        self.socket.sendto(message, address)

    def recv(self):
        return self.socket.recvfrom(1024)
        
    
