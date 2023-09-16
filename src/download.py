from modules.network_builder.network_builder import NetworkBuilder
from modules.parser import parse_download_args
from modules.logger_setup import logger_setup



if __name__ == "__main__":
    parsed_args = parse_download_args()
    # acceder a los argumentos parseados

    print(parsed_args)
    print(parsed_args.host)
    print(parsed_args.verbose)
    
    logger = logger_setup(parsed_args)
    # probar con -v y -q para ver los distintos niveles de log
    logger.critical("Esto es critico")
    logger.error("Es solo un error")
    logger.warning("Warning")
    logger.info("Te voy contando")
    logger.debug("Te cuento con mucho detalle")

    client = NetworkBuilder('CLIENT')\
            .set_logger(logger)\
            .set_host(parsed_args.host)\
            .set_port(parsed_args.port)\
            .build()
    

    client = Client(UDP_IP, UDP_PORT, None)
    client.connect()
    for x in range(0, 10):
        client.send(bytes('Hello World %s' % x, "utf-8"))
        time.sleep(5)
    client.send(b'exit')


    #TODO: seleccionar protocolo
    #TODO: descargar (?