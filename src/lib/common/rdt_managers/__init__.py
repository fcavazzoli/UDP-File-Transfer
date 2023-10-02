from .selective_repeat.receiver_handler import ReceiverHandler as SRReceiverHandler
from .selective_repeat.sender_handler import SenderHandler as SRSenderHandler
from .stop_and_wait.receiver_handler import ReceiverHandler as SWReceiverHandler
from .stop_and_wait.sender_handler import SenderHandler as SWSenderHandler

class RDTManagers:
    def get_manager(type, socket):
        if (type == 'selective-repeat'):
            return SRReceiverHandler(socket), SRSenderHandler(socket)
        elif (type == 'stop-and-wait'):
            return SWReceiverHandler(socket), SWSenderHandler(socket)
        raise Exception('Invalid type')
        
    def get_receiver_handler(type, socket):
        if (type == 'selective-repeat'):
            return SRReceiverHandler(socket)
        elif (type == 'stop-and-wait'):
            return SWReceiverHandler(socket)
        raise Exception('Invalid type')

        
    def get_sender_handler(type, socket):
        if (type == 'selective-repeat'):
            return SRSenderHandler(socket)
        elif (type == 'stop-and-wait'):
            return SWSenderHandler(socket)
        raise Exception('Invalid type')
