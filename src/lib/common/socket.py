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
            raise Exception('Destination address not set.')
        self.socket.sendto(message, self.address)
    
    def recv(self):
        try:
            data, addr = self.socket.recvfrom(DEFAULT_READABLE_SIZE)
            return data, addr
        except socket.timeout:
            raise TimeoutError("Timeout while waiting for data from the server.")
        except socket.error as e:
            raise Exception(f"Socket error during receive: {e}")
        except Exception as e:
            raise Exception(f"Error during receive: {e}")

    def change_destination(self, address):
        self.address = address
