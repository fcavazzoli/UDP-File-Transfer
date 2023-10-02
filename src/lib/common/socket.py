import socket
from queue import Queue
from threading import Thread

from lib.constants import DEFAULT_MESSAGE_SIZE, SEQ_NUM_SIZE, ACK_NUM_SIZE, HEADER_TYPE_SIZE
from lib.common.message import Message

DEFAULT_READABLE_SIZE = DEFAULT_MESSAGE_SIZE + SEQ_NUM_SIZE + ACK_NUM_SIZE + HEADER_TYPE_SIZE


class Socket:
    def bind(ip, port):
        socket = Socket()
        socket.socket.bind((ip, port))
        return socket

    def __init__(self, address=None):
        self.address = address
        self.socket = socket.socket(socket.AF_INET,  # Internet
                                    socket.SOCK_DGRAM)
        self.ack_received = Queue()
        self.data_received = Queue()


    def send(self, message):
        if (self.address is None):
            raise Exception('Destination address not set')
        self.socket.sendto(message, self.address)

    def recv(self):
        return  self.socket.recvfrom(DEFAULT_READABLE_SIZE)

    def _recv(self):
        packet, addr = self.socket.recvfrom(DEFAULT_READABLE_SIZE)
        message = Message.parse(packet)
        if(message.is_ack()):
            self.ack_received.put(message)
        elif(message.is_data()):
            self.data_received.put(message)

    def recv_ack(self):
        return self.ack_received.get()
    
    def recv_data(self):
        return self.data_received.get()


    def change_destination(self, address):
        self.address = address

    def listen(self):
        self.listener = SocketListener(self)
        self.listener.start()

class SocketListener(Thread):
    def __init__(self, socket):
        super(SocketListener, self).__init__()
        self.socket = socket

    def run(self):
        while (True):
            self.socket._recv()
