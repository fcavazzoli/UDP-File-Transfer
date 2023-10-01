from ..common.rdt_managers import RDTManagers
from ..common.socket import Socket
from ..common.configs import SingletonConfiguration


class Connection:
    socket = None
    receiverHandler = None

    def __init__(self, address):
        self.socket = Socket(address)
        self.rdt_type = SingletonConfiguration().get('protocol')

    def send(self, message):
        self.socket.send(message)

    def recv(self):
        return self.receiverHandler.recv()

    def listen(self):
        self.receiverHandler = RDTManagers.get_receiver_handler(self.rdt_type, self.socket)
