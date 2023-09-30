from os import getenv
import os
from lib.common.file_handler import FileHandler
from lib.constants import DEFAULT_MESSAGE_SIZE
from lib.helpers.network_builder import NetworkBuilder
from lib.common.parser import parse_upload_args
from lib.common.logger_setup import logger_setup


def upload(parsed_args):
    logger = logger_setup(parsed_args)
    
    host = parsed_args.host
    port = parsed_args.port
    protocol = parsed_args.protocol
    src = parsed_args.src
    name = parsed_args.name

    file = File.File(src, name)
    file.open("rb")

    #TODO: Lo dejo para poder utilizar la idea. Se envia la primera porcion del archivo, los primeros 1472 bytes. Se puede enviar este package para probar.
    #reads the first 1472 bytes of the file.
    #package = file.read(1472)

    client = NetworkBuilder('CLIENT')\
        .set_logger(logger)\
        .set_host(host)\
        .set_port(port)\
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
