import time
from lib.common.file_handler import FileHandler
from lib.common.message import Message

from lib.helpers.network_builder import NetworkBuilder
from lib.common.parser import parse_download_args
from lib.common.logger_setup import logger_setup


def download(parsed_args):
    logger = logger_setup(parsed_args)

    client = NetworkBuilder('CLIENT')\
        .set_logger(logger)\
        .set_host(parsed_args.host)\
        .set_port(parsed_args.port)\
        .set_protocol(parsed_args.protocol)\
        .build()

    try:
        logger.info("Client download started")
        client.connect()
        client.send(Message.build_metadata_payload(parsed_args.name, 'download'))
        file_handler = FileHandler('downloads/' + parsed_args.name, logger)
        while True:
            data = client.recv()
            opt = Message.unwrap_operation_type(data)
            if opt == 'METADATA':
                payload = Message.unwrap_payload_metadata(data)
                if payload == b'ERROR_FILE_DOES_NOT_EXIST':
                    break
            payload = Message.unwrap_payload_data(data)
            if payload == b'exit':
                print('Download completed')
                break
            file_handler.write_bytes(payload)
    except KeyboardInterrupt:
        logger.info("Client download stopped by user")
        exit(0)



if __name__ == "__main__":
    parsed_args = parse_download_args()
    download(parsed_args)
