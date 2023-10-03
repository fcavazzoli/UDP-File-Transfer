from lib.common.logger_setup import DummyLogger
from lib.constants import DEFAULT_IP, DEFAULT_PORT
from lib.common.configs import SingletonConfiguration


class NetworkBuilder:
    """
    Builder for network objects, either server or client. It is used to
    configure the network object (ip, port, type, etc) and building it.
    """

    def __init__(self, type):
        self.type = type
        self.logger = DummyLogger()
        self.port = DEFAULT_PORT
        self.host = DEFAULT_IP

    def set_logger(self, logger):
        self.logger = logger
        SingletonConfiguration().set('logger', logger)
        return self

    def set_port(self, port):
        self.port = int(port)
        return self

    def set_host(self, host):
        self.host = host
        return self

    def set_protocol(self, protocol):
        self.rdt = protocol
        SingletonConfiguration().set('protocol', protocol)
        return self

    def build(self):
        if self.type == 'SERVER':
            return self._build_server()
        elif self.type == 'CLIENT':
            return self._build_client()

    def _build_server(self):
        from lib.server import Server
        return Server(self.host, self.port)

    def _build_client(self):
        from lib.client import Client
        return Client(self.host, self.port)
