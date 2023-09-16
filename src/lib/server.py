import socket

from ConnectionsManagement import ConnectionsManagement

class Server:
    def __init__(self, udp_ip, port, logger):
        self.socket = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_DGRAM)
        self.socket.bind((udp_ip, port))
        self.logger = logger
        self.connections_management = ConnectionsManagement(self.socket)

    def serve(self):
        while True:
            data, addr = self.socket.recvfrom(1024)
            print("received message: %s" % data)
            self.connections_management.new_message(addr[0], addr[1], data)


