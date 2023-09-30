import socket

from lib.constants import DEFAULT_MESSAGE_SIZE, SEQ_NUM_SIZE

DEFAULT_READABLE_SIZE = DEFAULT_MESSAGE_SIZE + SEQ_NUM_SIZE


class Socket:
    def bind(ip, port):
        socket = Socket()
        socket.socket.bind((ip, port))
        return socket

    def __init__(self, address=None):
        self.address = address
        self.socket = socket.socket(socket.AF_INET,  # Internet
                                    socket.SOCK_DGRAM)

    def send(self, message):
        if (self.address is None):
            raise Exception('Destination address not set')
        self.socket.sendto(message, self.address)

    def recv(self):
        return self.socket.recvfrom(DEFAULT_READABLE_SIZE)

    def change_destination(self, address):
        self.address = address
