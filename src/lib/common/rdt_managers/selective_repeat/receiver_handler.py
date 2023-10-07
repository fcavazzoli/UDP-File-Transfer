from threading import Thread, Event

from lib.common.message import Message
from lib.common.configs import SingletonConfiguration
from lib.common.errors import ReceivingTimeOut
from lib.constants import RECEIVER_WINDOW_SIZE, RECEIVER_TIMEOUT

# La clase receiver handler es la interfaz entre la capa de aplicacion y el protocolo de transporte


class ReceiverHandler:

    packetHandler = None

    def __init__(self, socket):
        self.packetHandler = PacketHandler(socket)
        self.packetHandler.start()

    def recv(self):
        return self.packetHandler.recv()
    
    def close(self):
        self.packetHandler.close()
    
    def join(self):
        self.packetHandler.join()


# La clase packet handler es la que se encarga de recibir los mensajes y encolarlos en el orden correcto

class PacketHandler(Thread):
    def __init__(self, socket):
        super(PacketHandler, self).__init__()
        self.socket = socket
        self.window = Window(RECEIVER_WINDOW_SIZE)
        self.packet_to_read = Event()
        self.logger = SingletonConfiguration().get('logger')
        self.timeout_retries = 0
        self.is_closing = Event()

    def run(self):
        while (True):
            try:
                msg = self.socket.recv_data(RECEIVER_TIMEOUT)
                seq_num = msg.get_header().seq_num

                self.logger.debug('Received packet with seq_num: ' + str(seq_num))

                payload = msg.get_payload()

                if (self.window.packet_inside_window(seq_num)):
                    self.window.store(seq_num, payload)
                    self.send_ack(seq_num)

                elif (self.window.packet_was_received(seq_num)):
                    self.send_ack(seq_num)

                if (self.window.packets_to_read()):
                    self.packet_to_read.set()
            except ReceivingTimeOut as e:
                self.timeout_retries += 1
                if (self.timeout_retries == 5):
                    self.logger.debug('Max retries receiving packet')
                    break
                if (self.is_closing.is_set()):
                    self.logger.debug('Receiver Packet handler closed')
                    break
                


    def recv(self):
        if (not self.window.packets_to_read()):
            self.packet_to_read.wait()
        self.packet_to_read.clear()

        return self.window.next()

    def send_ack(self, ack_num):
        data = Message().set_header(0, ack_num, 'ACK').set_payload(b'').build()
        self.logger.debug('Sending ack: ' + str(ack_num))
        self.socket.send(data)

    def close(self):
        self.logger.debug('Closing receiver handler')
        self.is_closing.set()


# La clase window es la representacion de la ventana de recepcion

class Window:
    def __init__(self, size):
        self.max_window_size = size
        self.base = 0
        self.packets = {}

    def packet_exist(self, seq_num):
        return seq_num in self.packets

    def packet_inside_window(self, seq_num):
        return self.base <= seq_num < self.base + self.max_window_size

    def packet_was_received(self, seq_num):
        return seq_num < self.base

    def store(self, seq_num, packet):
        self.packets[seq_num] = packet

    def next(self):
        if (self.base not in self.packets):
            return None

        self.base += 1
        return self.packets.pop(self.base - 1)

    def is_full(self):
        return len(self.packets) == self.max_window_size

    def packets_to_read(self):
        return self.packet_exist(self.base)
