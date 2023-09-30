from ..common.rdt_managers.selective_repeat.receiver_handler import ReceiverHandler
from ..common.socket import Socket


class Connection:
    socket = None
    receiverHandler = None

    def __init__(self, address):
        self.socket = Socket(address)
        
    def send(self, message):
        self.socket.send(message)

    def recv(self):
        return self.receiverHandler.recv()
    
    def listen(self):
        self.receiverHandler = ReceiverHandler(self.socket)
        
    
