from threading import Thread, Event, Timer

from lib.common.message import Message

# La clase sender handler es la interfaz entre la capa de aplicacion y el protocolo de transporte


class SenderHandler:
    packetHandler = None
    window = None

    def __init__(self, socket):
        self.packetHandler = PacketHandler(socket)

    def send(self, data):
        return self.packetHandler.send(data)


class Packet:
    data = None
    timer = None
    ack = False
    seq_num = None

    def __init__(self, data, seq_num):
        self.data = data
        self.seq_num = seq_num

    def set_timer(self, resend):
        self.timer = Timer(10, resend, [self])
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


class PacketHandler():
    def __init__(self, socket):
        self.socket = socket
        self.next_seq_num = 0
        self.sended = {}

    def timeout(self, packet):
        packet.set_timer(self.timeout)
        self._send(packet.get_data())

    def _send(self, data):
        self.socket.send(data)

    def send(self, data):
        packet = Packet(data, self.next_seq_num)
        packet.set_timer(self.timeout)
        self.sended[self.next_seq_num] = packet
        print('SENDING', self.next_seq_num)
        self._send(packet.get_data())
        self.wait_ack()

    def wait_ack(self):
        while (True):
            msg = self.socket.recv_ack()
            print('ACK RECEIVED', msg.get_header().ack_num)
            ack = msg.get_header().ack_num
            if (ack == self.next_seq_num):
                self.sended[ack].cancel_timer()
                self.next_seq_num += 1
                return
