import struct

PACKET_FORMAT = "!II???"
"""
ver https://docs.python.org/3/library/struct.html#format-characters
! = byte order in network (big-endian)
I = unsigned int
? = boolean
B = unsigned char (1 byte)
"""





class Packet:
    """El payload está puesto como bytes ya que puede ser cualquier cosa: archivo, texto, enteros, etc.
    Por lo tanto antes de llamar a la función es necesario codificar el payload a bytes."""
    def __init__(self, seq_num, ack_num, ack_bit, syn_bit, fin_bit, data):
        # Header
        self.seq_num = seq_num      #32 bits
        self.ack_num = 0 if ack_num is None else ack_num            #32 bits
        self.ack_bit: bool = ack_bit      #1 byte (boolean)
        self.syn_bit: bool = syn_bit      #1 byte (boolean)
        self.fin_bit: bool = fin_bit      #1 byte (boolean)
        # self.data_size = data_size
        # self.protocol = "UDP"

        # Payload
        if(type(data) != bytes):
            raise Exception("El payload debe ser bytes")
        self.data: bytes = data


    def to_bytes(self) -> bytes:
        """Encodes the packet to a byte representation and returns it"""
        
        # encodea el header
        paquete_header_bytes = struct.pack(
            PACKET_FORMAT,
            self.seq_num,
            self.ack_num,
            self.ack_bit,
            self.syn_bit,
            self.fin_bit,
        )
        
        # encodea el checksum del header
        header_checksum = struct.pack("!B", self.calculate_checksum(paquete_header_bytes))

        # devuelve header, checksum y payload
        return paquete_header_bytes + header_checksum + self.data
    
    def from_bytes(self, packet_bytes: bytes):
        """Decodes the byte representation of a packet to a packet object and returns it"""

        #calculo el tamaño del header
        header_length = struct.calcsize(PACKET_FORMAT)
        header_length_checksum = header_length + 1        # +1 para el byte del checksum
        
        #decodifico el header (junto al checksum)
        header = struct.unpack(PACKET_FORMAT + 'B', packet_bytes[:header_length_checksum]) 

        # verificar checksum del header
        received_checksum = header[-1]
        calculated_checksum = self.calculate_checksum(packet_bytes[:header_length])
        if received_checksum != calculated_checksum:
            raise ValueError("Checksum incorrecto, se dropea el paquete")

        #decodifico el payload (desde el checksum en adelante)
        decoded_payload = packet_bytes[header_length_checksum:]
        return Packet(
            header[0],
            header[1],
            header[2],
            header[3],
            header[4],
            decoded_payload
        )
    

    def calculate_checksum(self, data):
        """
        Calcula un checksum super simple mediante la suma de los valores de los bytes en los datos.
        Si es necesario se puede modificar esta misma función para hacer un algoritmo más complejo.
        """
        #NOTE: con "from hashlib import md5"?

        checksum = 0
        for byte in data:
            checksum += byte
            checksum &= 0xFF  # Para mantener el checksum en 8 bits (byte)
        return checksum


# ejemplo de uso
# encodeo
data_en_formato_bytes = bytes("hola mundo loco", "utf-8")
paquete = Packet(333, 22222, False, False, True, data_en_formato_bytes)
paquete_encoded = paquete.to_bytes()
print(paquete_encoded)

#decodeo
paquete_decoded = paquete.from_bytes(paquete_encoded)
print("datos: ", paquete_decoded.data.decode())
