from queue import Queue

from ConnectionThread import ConnectionThread

class Connection:
    queue= None
    socket= None
    thread= None

    def __init__(self, connectionNumber, address, handshake_data):
        self.queue = Queue()


        handshake = bytes(handshake_data).decode('utf-8').split(' ')
        if(handshake[0] != 'handshake'):
            raise Exception('Invalid handshake')
        port = int(handshake[1])


        self.thread = ConnectionThread('Thread ' + str(connectionNumber), self.queue, address, port)
        self.thread.start()

    def received(self, message):
        self.queue.put(message)
