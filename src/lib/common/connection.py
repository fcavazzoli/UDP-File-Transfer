from socket import timeout

from .rdt_managers import RDTManagers
from .socket import Socket
from .configs import SingletonConfiguration


class Connection:
    socket = None
    receiverHandler = None
    connection_retry = 0

    def __init__(self):
        self.rdt_type = SingletonConfiguration().get('protocol')

    def connect(self, address):
        self.socket = Socket(address)
        while True: 
            try: 
                self.socket.set_timeout(10)
                self.socket.send(b'handshake')
                recv, addr = self.socket.recv()
                break
            except timeout as e:
                if self.connection_retry >= 5:
                    raise 'Socket connection timeout'
                self.connection_retry += 1
                print ('Connection timeout, retrying...')
                continue
        self.socket.set_timeout(None)
        self.socket.change_destination(addr)
        self.socket.listen()
        self.config_protocol()

    def accept(self, address):
        self.socket = Socket(address)
        self.socket.send(b'handshake Received')
        self.socket.listen()
        self.config_protocol()

    def send(self, message):
        self.senderHandler.send(message)

    def recv(self):
        return self.receiverHandler.recv()

    def config_protocol(self):
        self.receiverHandler = RDTManagers.get_receiver_handler(self.rdt_type, self.socket)
        self.senderHandler = RDTManagers.get_sender_handler(self.rdt_type, self.socket)
