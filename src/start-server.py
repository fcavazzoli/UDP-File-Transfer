from modules.network_builder.errors import NetworkBuilderError
from modules.network_builder.network_builder import NetworkBuilder
from modules.parser import parse_server_args
from modules.logger_setup import logger_setup

if __name__ == "__main__":
    parsed_args = parse_server_args()
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


    server = NetworkBuilder('SERVER')\
            .set_logger(logger)\
            .set_host(parsed_args.host)\
            .set_port(parsed_args.port)\
            .build() 
    try:
        server.serve()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
