from threading import Thread, Event, Timer

from lib.common.message import Message
from lib.common.configs import SingletonConfiguration
from lib.common.errors import ReceivingTimeOut
from lib.constants import SENDER_WINDOW_SIZE, SENDER_TIMEOUT, RECEIVER_TIMEOUT, MAX_RETRIES_WAITING

# La clase sender handler es la interfaz entre la capa de aplicacion y el protocolo de transporte


class SenderHandler:
    packetHandler = None
    window = None

    def __init__(self, socket):
        self.packetHandler = PacketHandler(socket)
        self.packetHandler.start()

    def send(self, data):
        return self.packetHandler.send(data)
    
    def close(self):
        self.packetHandler.close()

    def join(self):
        self.packetHandler.join()

    def messages_on_window(self):
        return self.packetHandler.window.messages_on_window()


class Packet:
    data = None
    timer = None
    ack = False
    seq_num = None

    def __init__(self, data, seq_num):
        self.data = data
        self.seq_num = seq_num

    def set_timer(self, resend):
        self.timer = Timer(SENDER_TIMEOUT, resend, [self])
        self.timer.start()

    def cancel_timer(self):
        self.timer.cancel()

    def set_ack(self):
        self.ack = True
        self.cancel_timer()

    def is_ack(self):
        return self.ack

    def get_data(self):
        return Message().set_header(self.seq_num, 0, 'DATA').set_payload(self.data).build()

# La clase packet handler es la que se encarga de encolar los mensajes a
# enviar, recibir los ack y enviarlos cuando es posible


class PacketHandler(Thread):
    def __init__(self, socket):
        super(PacketHandler, self).__init__()
        self.socket = socket
        self.window = Window(SENDER_WINDOW_SIZE)
        self.logger = SingletonConfiguration().get('logger')
        self.is_closing = Event()
        self.timeout_retries = 0

    def run(self):
        while (True):
            try:
                msg = self.socket.recv_ack(RECEIVER_TIMEOUT)
                ack = msg.get_header().ack_num
                self.logger.debug('Received ack: ' + str(ack))

                if (self.window.get_base() == ack):
                    self.window.clean_ack_packets()

                if (self.window.get_base() < ack):
                    self.window.mark_ack(ack)

                self.send_available_packets()
            except ReceivingTimeOut as e:
                self.timeout_retries += 1
                if (self.timeout_retries == MAX_RETRIES_WAITING):
                    self.logger.debug('Max retries receiving packet')
                    break
                if (self.is_closing.is_set()):
                    self.logger.debug('Sender Packet handler closed')
                    break    

    def timeout(self, packet):
        packet.set_timer(self.timeout)
        self.logger.debug('Timeout for packet: ' + str(packet.seq_num))
        self._send(packet.get_data())

    def _send(self, data):
        self.socket.send(data)

    def send_available_packets(self):
        while (self.window.is_message_to_send()):
            packet = self.window.next()
            packet.set_timer(self.timeout)
            self.logger.debug('Sending packet: ' + str(packet.seq_num))
            self._send(packet.get_data())

    def send(self, data):
        # if (self.window.is_full()):
        #     return False

        self.window.store(data)
        self.send_available_packets()

    def close(self):
        self.logger.debug('Closing sender handler')
        self.is_closing.set()


class Window:
    def __init__(self, size):
        self.max_window_size = size
        self.base = 0
        self.last_consumed = -1
        self.next_seq_num = 0
        self.packets = {}

    def store(self, data):
        self.packets[self.next_seq_num] = (Packet(data, self.next_seq_num))
        self.next_seq_num += 1

    def next(self):
        if (len(self.packets) == 0):
            return None
        packet = self.packets[self.last_consumed + 1]
        self.last_consumed += 1
        return packet

    def is_full(self):
        return len(self.packets) == self.max_window_size

    def clean_ack_packets(self):
        self.packets[self.base].set_ack()
        while (self.base in self.packets and self.packets[self.base].is_ack()):
            self.packets.pop(self.base)
            self.base += 1

    def increment_base(self):
        self.base += 1

    def get_base(self):
        return self.base

    def is_inside_window(self, seq_num):
        return self.base <= seq_num < self.base + self.max_window_size

    def mark_ack(self, seq_num):
        self.packets[seq_num].set_ack()

    def is_message_to_send(self):
        if (len(self.packets) == 0):
            return False

        return self.is_inside_window(self.last_consumed + 1) and self.last_consumed + 1 in self.packets
    
    def messages_on_window(self):
        return len(self.packets)
