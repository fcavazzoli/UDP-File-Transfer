from ..common.rdt_managers import RDTManagers
from ..common.socket import Socket
from ..common.configs import SingletonConfiguration


class Client:
    def __init__(self, remote_ip, remote_port, logger):
        self.socket = Socket((remote_ip, remote_port))
        self.logger = logger

    def _send(self, message):
        self.socket.send(message)

    def _receive(self):
        return self.socket.recv()

    def connect(self):
        self._send(bytes('handshake', "utf-8"))
        data, addr = self._receive()
        self.socket.change_destination(addr)
        self.socket.listen()
        rdt_type = SingletonConfiguration().get('protocol')
        self.sender_handler = RDTManagers.get_sender_handler(rdt_type, self.socket)

    def send(self, message):
        print('sending %s' %message)
        self.sender_handler.send(message)
