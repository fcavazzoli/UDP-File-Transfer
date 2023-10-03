from lib.helpers.network_builder import NetworkBuilder
from lib.common.parser import parse_server_args
from lib.common.logger_setup import logger_setup


def run_server(parsed_args):
    logger = logger_setup(parsed_args)

    server = NetworkBuilder('SERVER')\
        .set_logger(logger)\
        .set_host(parsed_args.host)\
        .set_port(parsed_args.port)\
        .set_protocol(parsed_args.protocol)\
        .build()
    try:
        logger.info("Server started")
        server.serve()
    except KeyboardInterrupt:
        #server.close()
        logger.info("Server stopped by user")
        exit()
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    parsed_args = parse_server_args()
    run_server(parsed_args)
