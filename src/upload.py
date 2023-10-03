from os import getenv
import os
from lib.common.file_handler import FileHandler
from lib.common.message import Message
from lib.constants import DEFAULT_MESSAGE_SIZE
from lib.helpers.network_builder import NetworkBuilder
from lib.common.parser import parse_upload_args
from lib.common.logger_setup import logger_setup

def calculate_file_size_in_packets(file_size):
    return (file_size / (DEFAULT_MESSAGE_SIZE)) + 1

def calculate_percentage(packets_received, file_size):
    return (packets_received / calculate_file_size_in_packets(file_size)) * 100

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
    packets_sended = 0

    # tenemos que restarle 1 porque el primer byte es el tipo de operacion
    file_bytes = FileHandler(parsed_args.name).read_bytes(DEFAULT_MESSAGE_SIZE-1)
    if file_bytes is None:
        exit(1)

    try:
        logger.info("Client upload started")
        client.connect()
        client.send(Message.build_metadata_payload(name, 'upload'))
        logger.info('Sent {0:.2f} % '.format(calculate_percentage(packets_sended, file_size)))
        for msg in file_bytes:
            packets_sended += 1
            client.send(Message.build_data_payload(msg))
            if(packets_sended % min(100, calculate_file_size_in_packets(file_size) // 2) == 0):
                logger.info('Sent {0:.2f} % '.format(calculate_percentage(packets_sended, file_size)))
        client.send(Message.build_data_payload(b'exit'))
        #client.close()
        logger.info("Client upload completed")
    except KeyboardInterrupt:
        logger.info("Client upload stopped by user")
        exit(0)
    except Exception:
        logger.error("Client upload stopped unexpectedly")



if __name__ == "__main__":
    parsed_args = parse_upload_args()
    upload(parsed_args)
