import time
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
        for x in range(20):
            client.send(Message.build_data_payload(b'SEQ %i' % x))
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Client download stopped by user")
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    parsed_args = parse_download_args()
    download(parsed_args)
