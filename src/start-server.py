from modules.network_builder import NetworkBuilder
from modules.parser import parse_server_args
from modules.logger_setup import logger_setup

def run_server(parsed_args):
    logger = logger_setup(parsed_args)

    server = NetworkBuilder('SERVER')\
            .set_logger(logger)\
            .set_host(parsed_args.host)\
            .set_port(parsed_args.port)\
            .build() 
    try:
        server.serve()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    parsed_args = parse_server_args()
    run_server(parsed_args)
