import struct

FORMATO_PAQUETE = "iii"             #ver https://docs.python.org/3/library/struct.html#format-characters

class Packet:
    def __init__(self, seq_num, ack_num, ack_bit, syn_bit, fin_bit, data_size, data):


        #header
        self.seq_num = seq_num
        self.ack_num = ack_num
        # self.ack_num = 0 if ack_num is None else ack_num
        self.ack_bit = ack_bit
        # self.syn_bit = syn_bit        #iniciar conexion ??
        # self.fin_bit = fin_bit        #terminar conexion ??
        self.data_size = data_size
        self.protocol = "UDP"
        # self.checksum = checksum

        #payload
        self.data = data

    def to_bytes(self):
        """Encodes the packet to a byte representation. Using struct.pack() to encode the packet to bytes with the following format:
        
        """        
        paquete_bytes = struct.pack("iii", self.seq_num, 20, 44)
        
        print(paquete_bytes)
        print(struct.unpack(FORMATO_PAQUETE, paquete_bytes))
    
    def from_bytes(self):
        """Decodes the byte representation of a packet to a packet object"""
        pass

paquete = Packet(11, 22, 33, 44, 55, 66, 77)
paquete.to_bytes()