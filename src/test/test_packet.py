import unittest
from lib.common.packet import Packet

class TestPacket(unittest.TestCase):
    def test_packet_payload_type_check(self):
        print("Testing test_packet_payload_type_check...")
        # Test that the constructor raises an exception if the payload is not bytes
        payload = "This is not bytes"
        with self.assertRaises(Exception):
            Packet(1, 2, False, False, False, payload)

if __name__ == '__main__':
    unittest.main()