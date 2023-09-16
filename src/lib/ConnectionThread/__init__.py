import threading
import socket

class ConnectionThread(threading.Thread):

    queue = None

    def __init__(self, name, queue, address, port):
        super(ConnectionThread, self).__init__()
        self.queue = queue
        self.name = name
        self.socket = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_DGRAM)
        self.client_address = address
        self.client_port = port
        
    
    def run(self):

        self.socket.sendto(bytes('Handshake Received %s' % self.name, "utf-8"), (self.client_address, self.client_port))

        while(True):
            data = self.queue.get()
            response = bytes('OK Received %s' % self.name, "utf-8")
            self.socket.sendto(response, (self.client_address, self.client_port))
            if(data == b'exit'):
                break

        self.socket.sendto(bytes('EXIT Received %s' % self.name, "utf-8"), (self.client_address, self.client_port))
            