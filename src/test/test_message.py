import unittest
from lib.common.message import Message

class TestMessageClass(unittest.TestCase):

    def test_set_header(self):
        print("Testing test_set_header...")
        msg = Message()
        msg.set_header(1, 2, 'DATA')
        self.assertEqual(msg.type, 0)  # 'DATA' maps to 0 in HEADER_TYPE
        self.assertEqual(msg.seq_num, 1)
        self.assertEqual(msg.ack_num, 2)

    def test_set_payload(self):
        print("Testing test_set_payload...")
        msg = Message()
        msg.set_payload(b'Hello, World!')
        self.assertEqual(msg.payload, b'Hello, World!')

    def test_get_header(self):
        print("Testing test_get_header...")
        msg = Message()
        msg.type = 1
        msg.seq_num = 3
        msg.ack_num = 4
        header = msg.get_header()
        self.assertEqual(header.type, 1)
        self.assertEqual(header.seq_num, 3)
        self.assertEqual(header.ack_num, 4)

    def test_get_payload(self):
        print("Testing test_get_payload...")
        msg = Message()
        msg.payload = b'Hello, World!'
        payload = msg.get_payload()
        self.assertEqual(payload, b'Hello, World!')

if __name__ == '__main__':
    unittest.main()
