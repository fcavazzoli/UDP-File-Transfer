from os import getenv
import os
import time
from lib.File import File
from lib.common.file_handler import FileHandler
from lib.common.message import Message
from lib.constants import DEFAULT_MESSAGE_SIZE
from lib.helpers.network_builder import NetworkBuilder
from lib.common.parser import parse_upload_args
from lib.common.logger_setup import logger_setup

# Define the maximum number of retry attempts
MAX_RETRIES = 3

# Define the delay between retry attempts (in seconds)
RETRY_DELAY = 5

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

    file_path = src if src is not None else name
    if file_path is None:
        logger.error("Missing arguments --name or --src are required")
        exit(1)

    file_bytes = FileHandler(parsed_args.name, logger).read_bytes(DEFAULT_MESSAGE_SIZE)
    if file_bytes is None:
        exit(1)

    #Another way to handle the files: 
    #file = File(src, name)
    #file.open ("rb")
    #file_bytes = file.read(1472)

    for retry_count in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Client upload attempt {retry_count}")
            client.connect()
            client.send(Message.build_metadata_payload(name))
            for msg in file_bytes:
                client.send(Message.build_data_payload(msg))
            logger.info("Message sent")
            client.send(Message.build_data_payload(b'exit'))
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Error during upload attempt {retry_count}.")
            if retry_count < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error("Max retries reached. Upload failed.")
                break
        finally:
            if client.socket and retry_count >= MAX_RETRIES:
                logger.info("Connection closed.")
                client.close()  # Close the connection whether it succeeded or failed

if __name__ == "__main__":
    parsed_args = parse_upload_args()
    upload(parsed_args)
