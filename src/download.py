import time

from lib.helpers.network_builder import NetworkBuilder
from lib.common.parser import parse_download_args
from lib.common.logger_setup import logger_setup


def download(parsed_args):
    logger = logger_setup(parsed_args)

    client = NetworkBuilder('CLIENT')\
        .set_logger(logger)\
        .set_host(parsed_args.host)\
        .set_port(parsed_args.port)\
        .build()

    try:
        client.connect()
        for x in range(0, 10):
            client.send(bytes('Hello World %s' % x, "utf-8"))
            time.sleep(5)
        client.send(b'exit')
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    parsed_args = parse_download_args()
    download(parsed_args)
