import threading
import socket

class ConnectionThread(threading.Thread):

    queue = None

    def __init__(self, name, queue, address):
        super(ConnectionThread, self).__init__()
        self.queue = queue
        self.name = name
        self.socket = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_DGRAM)
        self.client_address = address
        
    
    def run(self):

        self.socket.sendto(bytes('Handshake Received %s' % self.name, "utf-8"), self.client_address)

        while(True):
            data = self.queue.get()
            response = bytes('OK Received %s' % self.name, "utf-8")
            self.socket.sendto(response, self.client_address)
            if(data == b'exit'):
                break

        self.socket.sendto(bytes('EXIT Received %s' % self.name, "utf-8"), self.client_address)
            