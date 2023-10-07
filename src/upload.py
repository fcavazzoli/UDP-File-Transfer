from os import getenv
import os

from time import sleep

from lib.common.file_handler import FileHandler
from lib.common.message import Message
from lib.constants import DEFAULT_MESSAGE_SIZE
from lib.helpers.network_builder import NetworkBuilder
from lib.common.parser import parse_upload_args
from lib.common.logger_setup import logger_setup
from lib.common.errors import ConnectionMaxRetriesException

def calculate_file_size_in_packets(file_size):
    return (file_size / (DEFAULT_MESSAGE_SIZE)) + 1

def calculate_percentage(remaining_packets, packets_to_send):
    return ((packets_to_send - remaining_packets) / packets_to_send) * 100

def upload(parsed_args):
    logger = logger_setup(parsed_args)

    host = parsed_args.host
    port = parsed_args.port
    protocol = parsed_args.protocol
    src = parsed_args.src
    name = parsed_args.name

    client = NetworkBuilder('CLIENT')\
        .set_logger(logger)\
        .set_host(host)\
        .set_port(port)\
        .set_protocol(protocol)\
        .build()

    file_path = parsed_args.src if parsed_args.src is not None else parsed_args.name
    if file_path is None:
        logger.error("Missing arguments --name or --src are required")
        exit(1)

    file_size = os.path.getsize(file_path)
    packets_to_send = calculate_file_size_in_packets(file_size)

    logger.debug("Will send {0} bytes on {1} packets".format(file_size, packets_to_send))

    # tenemos que restarle 1 porque el primer byte es el tipo de operacion
    file_bytes = FileHandler(parsed_args.name).read_bytes(DEFAULT_MESSAGE_SIZE-1)
    if file_bytes is None:
        exit(1)

    try:
        logger.info("Client upload started")
        client.connect()
        client.send(Message.build_metadata_payload(name, 'upload'))
        for msg in file_bytes:
            client.send(Message.build_data_payload(msg))
        client.send(Message.build_data_payload(b'exit'))

        while (True):
            remaining_packets = client.messages_on_window()
            if (remaining_packets == 0):
                break
            sleep(1)
            logger.info("Sended {0:.2f} %".format(calculate_percentage(remaining_packets, packets_to_send)))
            

        client.close()
        logger.info("Client upload completed")
    except KeyboardInterrupt:
        logger.info("Client upload stopped by user")
        client.close()
        exit(0)
    except ConnectionMaxRetriesException as e: 
        logger.error("Connection failed: {}".format(e))
    except Exception as e:
        logger.error("Client upload stopped unexpectedly with error " + str(e))




if __name__ == "__main__":
    parsed_args = parse_upload_args()
    upload(parsed_args)
