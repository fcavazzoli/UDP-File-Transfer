from types import SimpleNamespace

OPT_TYPE = {
    'METADATA': 0,
    'DATA': 1,
}

HEADER_TYPE = {
    'DATA': 0,
    'ACK': 1,
}


class Message:
    def __init__(self):
        self.header = None
        self.payload = None

    def set_header(self, seq_num, ack_num, type):
        self.type = HEADER_TYPE[type]
        self.seq_num = seq_num
        self.ack_num = ack_num
        return self

    def set_payload(self, payload):
        self.payload = payload
        return self

    def get_header(self):
        return SimpleNamespace(type=self.type, seq_num=self.seq_num, ack_num=self.ack_num)

    def get_payload(self):
        return self.payload

    def get_operation(self):
        return list(OPT_TYPE.keys())[list(OPT_TYPE.values()).index(int.from_bytes(self.payload[:1], byteorder='big'))]

    def build(self):
        header_byte = self.type.to_bytes(4, byteorder='big') + self.seq_num.to_bytes(4,
                                                                                     byteorder='big') + self.ack_num.to_bytes(4, byteorder='big')
        return header_byte + self.payload

    def parse(message):
        type = Message.unwrap_header_type(message)
        seq_num = int.from_bytes(message[4:8], byteorder='big')
        ack_num = int.from_bytes(message[8:12], byteorder='big')
        payload = message[12:]
        return Message().set_header(seq_num, ack_num, type).set_payload(payload)

    def build_metadata_payload(file_name, action):
        operation_type = OPT_TYPE['METADATA'].to_bytes(1, byteorder='big')
        action_type = 1 if action == 'upload' else 0
        action_type_bytes = action_type.to_bytes(1, byteorder='big')
        file_name_bytes = bytes(file_name, 'utf-8')
        print('file_name_bytes: ', operation_type + action_type_bytes + file_name_bytes)
        return operation_type + action_type_bytes + file_name_bytes

    def build_data_payload(data):
        operation_type = OPT_TYPE['DATA'].to_bytes(1, byteorder='big')
        return operation_type + data

    def unwrap_operation_type(data):
        return list(OPT_TYPE.keys())[list(OPT_TYPE.values()).index(int.from_bytes(data[:1], byteorder='big'))]

    def unwrap_header_type(header):
        return list(HEADER_TYPE.keys())[list(HEADER_TYPE.values()).index(int.from_bytes(header[:4], byteorder='big'))]

    def unwrap_action_type(data):
        return int.from_bytes(data[1:2], byteorder='big')

    def unwrap_payload_data(payload):
        return payload[2:]

    def is_ack(self):
        return self.type == HEADER_TYPE['ACK']

    def is_data(self):
        return self.type == HEADER_TYPE['DATA']
