from threading import Thread, Event

from lib.common.message import Message

# La clase receiver handler es la interfaz entre la capa de aplicacion y el protocolo de transporte


class ReceiverHandler:

    packetHandler = None

    def __init__(self, socket):
        self.packetHandler = PacketHandler(socket)

    def recv(self):
        return self.packetHandler.recv()


# La clase packet handler es la que se encarga de recibir los mensajes y encolarlos en el orden correcto

class PacketHandler(Thread):
    def __init__(self, socket):
        super(PacketHandler, self).__init__()
        self.socket = socket
        self.next_seq_num = 0

    def recv(self):
            while True: 
                packet, addr = self.socket.recv()
                msg = Message.parse(packet)
                seq_num = msg.get_header()
                payload = msg.get_payload()

                self.send_ack(seq_num)

                if(seq_num == self.next_seq_num):
                    self.next_seq_num += 1
                    break

            return payload


    def send_ack(self, ack_num):
        self.socket.send(("ACK " + str(ack_num)).encode())

