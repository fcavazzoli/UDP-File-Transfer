from .selective_repeat.receiver_handler import ReceiverHandler as SRReceiverHandler
from .selective_repeat.sender_handler import SenderHandler as SRSenderHandler
from .stop_and_wait.receiver_handler import ReceiverHandler as SWReceiverHandler
from .stop_and_wait.sender_handler import SenderHandler as SWSenderHandler

class RDTManagers:
    @staticmethod
    def get_manager(type, socket):
        handler_map = {
            'selective-repeat': (SRReceiverHandler, SRSenderHandler),
            'stop-and-wait': (SWReceiverHandler, SWSenderHandler),
        }
        receiver_handler, sender_handler = handler_map.get(type, (None, None))
        if receiver_handler and sender_handler:
            return receiver_handler(socket), sender_handler(socket)
        raise Exception('Invalid type')

    @staticmethod
    def get_receiver_handler(type, socket):
        handler_map = {
            'selective-repeat': SRReceiverHandler,
            'stop-and-wait': SWReceiverHandler,
        }
        receiver_handler = handler_map.get(type)
        if receiver_handler:
            return receiver_handler(socket)
        raise Exception('Invalid type')

    @staticmethod
    def get_sender_handler(type, socket):
        handler_map = {
            'selective-repeat': SRSenderHandler,
            'stop-and-wait': SWSenderHandler,
        }
        sender_handler = handler_map.get(type)
        if sender_handler:
            return sender_handler(socket)
        raise Exception('Invalid type')