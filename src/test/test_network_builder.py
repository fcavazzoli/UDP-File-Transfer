import unittest
from unittest.mock import MagicMock
from lib.common.logger_setup import DummyLogger
from lib.constants import DEFAULT_IP, DEFAULT_PORT
from lib.common.configs import SingletonConfiguration
from lib.helpers.network_builder import NetworkBuilder

class TestNetworkBuilder(unittest.TestCase):
    def test_default_values(self):
        print("Testing test_default_values...")
        builder = NetworkBuilder('SERVER')
        self.assertEqual(builder.type, 'SERVER')
        self.assertIsInstance(builder.logger, DummyLogger)
        self.assertEqual(builder.port, DEFAULT_PORT)
        self.assertEqual(builder.host, DEFAULT_IP)

    def test_set_logger(self):
        print("Testing test_set_logger...")
        builder = NetworkBuilder('SERVER')
        logger = MagicMock()
        builder.set_logger(logger)
        self.assertIs(builder.logger, logger)
        self.assertIs(SingletonConfiguration().get('logger'), logger)

    def test_set_port(self):
        print("Testing test_set_port...")
        builder = NetworkBuilder('SERVER')
        new_port = 12345
        builder.set_port(new_port)
        self.assertEqual(builder.port, new_port)

    def test_set_host(self):
        print("Testing test_set_host...")
        builder = NetworkBuilder('SERVER')
        new_host = '127.0.0.1'
        builder.set_host(new_host)
        self.assertEqual(builder.host, new_host)

    def test_set_protocol(self):
        print("Testing test_set_protocol...")
        builder = NetworkBuilder('SERVER')
        protocol = 'selective-repeat'
        builder.set_protocol(protocol)
        self.assertEqual(SingletonConfiguration().get('protocol'), protocol)

if __name__ == '__main__':
    unittest.main()
