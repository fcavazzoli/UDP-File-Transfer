from lib.helpers.network_builder import NetworkBuilder
from lib.common.parser import parse_upload_args
from lib.common.logger_setup import logger_setup
import lib.File as File

def upload(parsed_args):
    logger = logger_setup(parsed_args)

    host = parsed_args.host
    port = parsed_args.port
    protocol = parsed_args.protocol
    src = parsed_args.src
    name = parsed_args.name

    file = File.File(src, name)
    file.open("rb")

    #TODO: Lo dejo para poder utilizar la idea. Se envia la primera porcion del archivo, los primeros 1472 bytes.
    #Descomentar linea para probar > client.send(package) y comentar la linea client.send(msg).
    #reads the first 1472 bytes of the file.
    #package = file.read(1472)

    client = NetworkBuilder('CLIENT')\
        .set_logger(logger)\
        .set_host(host)\
        .set_port(port)\
        .build()

    msg = bytes('Hola server', 'utf-8')
    # TODO: seleccionar protocolo
    # TODO: subir (?

    try:
        logger.info("Client upload started")
        client.send(msg)
        #TODO: 
        # client.send(package)
        logger.info("Message sent")
        client.send(b'exit')
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(e)



if __name__ == "__main__":
    parsed_args = parse_upload_args()
    upload(parsed_args)
