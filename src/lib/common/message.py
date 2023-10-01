OPT_TYPE = {
    'METADATA': 0,
    'DATA': 1,
}
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

    def get_operation(self):
        return list(OPT_TYPE.keys())[list(OPT_TYPE.values()).index(int.from_bytes(self.payload[:1], byteorder='big'))]
    
    def build(self):
        header_byte = self.header.to_bytes(4, byteorder='big')
        return header_byte + self.payload

    def parse(message):
        header = int.from_bytes(message[:4], byteorder='big')
        payload = message[4:]
        return Message().set_header(header).set_payload(payload)
     
    def build_metadata_payload(file_name, file_size=0):
        operation_type = OPT_TYPE['METADATA'].to_bytes(1, byteorder='big')
        file_name_bytes = bytes(file_name, 'utf-8')
        file_size_bytes = file_size.to_bytes(4, byteorder='big')
        return operation_type + file_name_bytes
    
    def build_data_payload(data):
        operation_type = OPT_TYPE['DATA'].to_bytes(1, byteorder='big')
        return operation_type + data
    
    def unwrap_operation_type(payload):
        print(f'payload: {payload}')
        return list(OPT_TYPE.keys())[list(OPT_TYPE.values()).index(int.from_bytes(payload[:1], byteorder='big'))]
    
    def unwrap_payload_data(payload):
        return payload[1:]