import socket

from ..common.rdt_managers.selective_repeat.receiver_handler import ReceiverHandler


class Connection:
    address = None
    socket = None
    receiverHandler = None

    def __init__(self, address):
        self.address = address
        self.socket = socket.socket(socket.AF_INET,  # Internet
                                    socket.SOCK_DGRAM)
        
    def send(self, message):
        self.socket.sendto(message, self.address)

    def recv(self):
        return self.receiverHandler.recv()
    
    def listen(self):
        self.receiverHandler = ReceiverHandler(self.socket, self.address)
        
    
