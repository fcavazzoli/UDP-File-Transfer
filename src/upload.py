from os import getenv
import os
from lib.common.file_handler import FileHandler
from lib.constants import DEFAULT_MESSAGE_SIZE
from lib.helpers.network_builder import NetworkBuilder
from lib.common.parser import parse_upload_args
from lib.common.logger_setup import logger_setup


def upload(parsed_args):
    logger = logger_setup(parsed_args)

    client = NetworkBuilder('CLIENT')\
        .set_logger(logger)\
        .set_host(parsed_args.host)\
        .set_port(parsed_args.port)\
        .set_protocol(parsed_args.protocol)\
        .build()

    file_path = parsed_args.src if parsed_args.src is not None else parsed_args.name
    if file_path is None:
        logger.error("Missing arguments --name or --src are required")
        exit(1)

    file_bytes = FileHandler(parsed_args.name, logger).read_bytes(DEFAULT_MESSAGE_SIZE)
    print(file_bytes)
    if file_bytes is None:
        exit(1)

    try:
        logger.info("Client upload started")
        client.connect()
        # [b'Aguante ', b'Boca']
        for msg in file_bytes:
            client.send(msg)
        logger.info("Message sent")
        client.send(b'exit')
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    parsed_args = parse_upload_args()
    upload(parsed_args)
