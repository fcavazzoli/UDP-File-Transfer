class Message:
    def __init__(self):
        self.header = None
        self.payload = None


    def set_header(self, seq_num):
        self.header = seq_num
        return self
    
    def set_payload(self, payload):
        self.payload = payload
        return self
    
    def get_header(self):
        return self.header
    
    def get_payload(self):
        return self.payload

    def build(self):
        header_byte = self.header.to_bytes(4, byteorder='big')
        return header_byte + self.payload
    