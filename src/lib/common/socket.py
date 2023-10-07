import socket
from queue import Queue, Empty
from threading import Thread, Event

from lib.constants import DEFAULT_MESSAGE_SIZE, SEQ_NUM_SIZE, ACK_NUM_SIZE, HEADER_TYPE_SIZE, RECEIVER_TIMEOUT, MAX_RETRIES_WAITING
from lib.common.message import Message
from lib.common.configs import SingletonConfiguration
from lib.common.errors import ReceivingTimeOut

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
        self.logger = SingletonConfiguration().get('logger')


    def send(self, message):
        if (self.address is None):
            raise Exception('Destination address not set')
        self.socket.sendto(message, self.address)

    def recv(self):
        return self.socket.recvfrom(DEFAULT_READABLE_SIZE)

    def _recv(self):
        packet, addr = self.socket.recvfrom(DEFAULT_READABLE_SIZE)
        message = Message.parse(packet)
        if (message.is_ack()):
            self.ack_received.put(message)
        elif (message.is_data()):
            self.data_received.put(message)

    def recv_ack(self, timeout=None):
        try:
            return self.ack_received.get(timeout=timeout)
        except Empty:
            raise ReceivingTimeOut()

    def recv_data(self, timeout=None):
        try:
            return self.data_received.get(timeout=timeout)
        except Empty:
            raise ReceivingTimeOut()

    def change_destination(self, address):
        self.address = address

    def listen(self):
        self.listener = SocketListener(self)
        self.listener.start()

    def set_timeout(self, timeout):
        self.socket.settimeout(timeout)

    def close(self):
        self.logger.debug('Closing socket')
        self.listener.close()

    def join(self):
        self.listener.join()


class SocketListener(Thread):
    def __init__(self, socket):
        super(SocketListener, self).__init__()
        self.socket = socket
        self.closing = Event()
        self.logger = SingletonConfiguration().get('logger')
        self.socket.set_timeout(RECEIVER_TIMEOUT)
        self.timeout_retries = 0


    def run(self):
        while (True):
            try:
                self.closing = Event()
                self.socket._recv()
                self.timeout_retries = 0
            except socket.timeout:
                if (self.closing.is_set()):
                    self.logger.debug('Socket listener closed')
                    break
                if (self.timeout_retries == MAX_RETRIES_WAITING):
                    self.logger.debug('Socket listener timed out')
                    break
                
                continue


    def close(self):
        self.closing.set()

    
