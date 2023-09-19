from lib.helpers.network_builder import NetworkBuilder
from lib.common.parser import parse_upload_args
from lib.common.logger_setup import logger_setup


def upload(parsed_args):
    logger = logger_setup(parsed_args)

    client = NetworkBuilder('CLIENT')\
        .set_logger(logger)\
        .set_host(parsed_args.host)\
        .set_port(parsed_args.port)\
        .build()

    msg = bytes('Hola server', 'utf-8')
    # TODO: seleccionar protocolo
    # TODO: subir (?

    try:
        logger.info("Client upload started")
        client.send(msg)
        logger.info("Mensaje enviado")
        client.send(b'exit')
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    parsed_args = parse_upload_args()
    upload(parsed_args)
