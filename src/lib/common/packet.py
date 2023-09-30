import struct

PACKET_FORMAT = "!II???"
"""
ver https://docs.python.org/3/library/struct.html#format-characters
! = byte order in network (big-endian)
I = unsigned int
? = boolean
"""

class Packet:
    def __init__(self, seq_num, ack_num, ack_bit, syn_bit, fin_bit, data):
        # Header
        self.seq_num = seq_num      #32 bits
        self.ack_num = 0 if ack_num is None else ack_num            #32 bits
        self.ack_bit = ack_bit      #1 byte (boolean)
        self.syn_bit = syn_bit      #1 byte (boolean)
        self.fin_bit = fin_bit      #1 byte (boolean)
        # self.data_size = data_size
        # self.protocol = "UDP"
        # self.checksum = checksum

        # Payload
        self.data = data


    def to_bytes(self) -> bytes:
        """Encodes the packet to a byte representation and returns it"""
        #encodea el payload
        payload_to_encode: bytes = bytes(self.data, "utf-8")
        #encodea el header
        paquete_header_bytes = struct.pack(
            PACKET_FORMAT,
            self.seq_num,
            self.ack_num,
            self.ack_bit,
            self.syn_bit,
            self.fin_bit,
        )
        return paquete_header_bytes + payload_to_encode
    
    def from_bytes(self, packet_bytes: bytes):
        """Decodes the byte representation of a packet to a packet object and returns it"""

        # verificar checksum

        #calculo el tamaño del header
        header_length = struct.calcsize(PACKET_FORMAT)
        #decodifico el header
        decoded_packet = struct.unpack(PACKET_FORMAT, packet_bytes[:header_length])
        #decodifico el payload
        decoded_payload = packet_bytes[header_length:]
        
        return Packet(
            decoded_packet[0],
            decoded_packet[1],
            decoded_packet[2],
            decoded_packet[3],
            decoded_packet[4],
            decoded_payload.decode()
        )


paquete = Packet(11, 22, False, False, True, "hola mundo")
paquete_encoded = paquete.to_bytes()
print(paquete_encoded)

paquete_decoded = paquete.from_bytes(paquete_encoded)


print("paquete_decoded.data", paquete_decoded.ack_num)

