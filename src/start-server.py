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

    #TODO: seleccionar protocolo
    #TODO: server stuff (?