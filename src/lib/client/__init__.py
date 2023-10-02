import socket
from lib.common.logger_setup import logger_setup
from ..common.rdt_managers import RDTManagers
from ..common.socket import Socket
from ..common.configs import SingletonConfiguration


class Client:
    def __init__(self, remote_ip, remote_port, logger):
        self.socket = Socket((remote_ip, remote_port))
        self.logger = logger

    def _send(self, message):
        try:
            self.socket.send(message)
        except self.socket.error as e:
            print(f"Failed to send message: {e}")
            self.logger.error(f"Failed to send message: {e}")        

    def _receive(self):
        try:
            self.socket.socket.settimeout(10)
            data, addr = self.socket.recv()
            return data, addr
        except socket.timeout:
            self.logger.error("Timeout while waiting for a response from the server.")
        except Exception as e:
            self.logger.error(f"Couldn't receive any data.")

    def connect(self):
        try:
            self.logger.info("Connecting to server...")
            self._send(bytes('handshake', "utf-8"))
            self.logger.info("Sending handshake message... please wait.")
            data, addr = self._receive()
            self.logger.info(f"Received data: {data}, Address: {addr}")
            self.socket.change_destination(addr)
            self.logger.info("Changed destination")
            rdt_type = SingletonConfiguration().get('protocol')
            self.logger.info(f"Selected protocol: {rdt_type}")
            self.sender_handler = RDTManagers.get_sender_handler(rdt_type, self.socket)
            self.logger.info("The connection has been established.")
        except Exception as e:
            self.logger.error(f"Couldn't establish a connection.")

    def send(self, message):
        print(f'Sending: {message}')
        self.sender_handler.send(message)

    def close(self):
        if self.socket.socket:
            self.socket.socket.close()
            print("Client socket closed.")
        else: 
            print("Couldn't close client socket.")
