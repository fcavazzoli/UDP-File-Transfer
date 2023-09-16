from lib.constants import DEFAULT_IP, DEFAULT_PORT

class NetworkBuilder:
    def __init__(self, type):
        self.type = type
        self.logger = None
        self.port = DEFAULT_PORT
        self.host = DEFAULT_IP

    def set_logger(self, logger):
        self.logger = logger
        return self
    
    def set_port(self, port):
        self.port = int(port)
        return self
    
    def set_host(self, host):
        self.host = host
        return self
    
    def build(self):
        if self.type == 'SERVER':
            return self._build_server()
        elif self.type == 'CLIENT':
            return self._build_client()
        
    def _build_server(self):
        from lib.server import Server
        return Server(self.host, self.port, self.logger)
    
    def _build_client(self):
        from lib.client import Client
        return Client(self.host, self.port, self.logger)