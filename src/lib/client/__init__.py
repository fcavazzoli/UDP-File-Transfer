from ..common.rdt_managers.selective_repeat.sender_handler import SenderHandler as Sender
from ..common.socket import Socket


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
        self.sender_handler = Sender(self.socket)

    def send(self, message):
        print(f'sending {message}')
        self.sender_handler.send(message)
