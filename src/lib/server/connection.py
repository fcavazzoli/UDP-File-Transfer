import socket

class Connection:
    address = None
    sock = None

    def __init__(self, address):
        self.address = address
        self.sock = socket.socket(socket.AF_INET,    # AF_INET = IPv4
                                    socket.SOCK_DGRAM)  # SOCK_DGRAM = UDP
        
    def send(self, message):
        self.sock.sendto(message, self.address)

    def recv(self):
        return self.sock.recvfrom(1024)
        
    
