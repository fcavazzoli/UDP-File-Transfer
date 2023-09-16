import logging
from typing import Any
from lib.constants import DEFAULT_LOG_FILE_NAME
"""
Es la configuración del Logger, para obtener una instancia de logger se debe llamar a logger_setup() y
pasarle como argumento los argumentos parseados por argparse
* El logger tiene dos handlers, por archivo y por consola
* Por linea de comandos es posible establecer la verbosidad del logger
* Tanto upload, download y start-server usan el mismo logger

Resumen de niveles, de más bajo a más alto:
    CRITICAL       ^
    ERROR          |   <- quiet
    WARNING        |
    INFO           |   <- default
    DEBUG          |   <- verbose
"""


def logger_setup(parsed_args):
    log_file_name = DEFAULT_LOG_FILE_NAME
    logger = logging.getLogger()

    # determina que nivel de log se va a mostrar (verbosidad en este caso)
    if parsed_args.quiet:
        log_level = logging.ERROR
    elif parsed_args.verbose:
        log_level = logging.DEBUG
    else:
        # por default el logger es INFO
        log_level = logging.INFO

    logger.setLevel(log_level)

    # handler para el archivo
    formatter_archivo = logging.Formatter(
        fmt='%(asctime)s:%(levelname)-8s [%(filename)s] --- %(message)s',
        datefmt='%d-%m-%y %H:%M:%S')
    archivo_handler = logging.FileHandler(log_file_name)
    archivo_handler.setLevel(logging.DEBUG)
    archivo_handler.setFormatter(formatter_archivo)
    logger.addHandler(archivo_handler)

    # handler por consola (personalizable por linea de comandos)
    formatter_consola = logging.Formatter('%(levelname)-8s %(message)s')
    consola_handler = logging.StreamHandler()
    consola_handler.setLevel(log_level)
    consola_handler.setFormatter(formatter_consola)
    logger.addHandler(consola_handler)

    return logger


class DummyLogger:
    def __init__(self):
        self.warning_printed = False

    def debug(self, msg, *args: Any, **kwargs: Any):
        if not self.warning_printed:
            print('WARNING: EL LOGGER NO ESTA CONFIGURADO')
            self.warning_printed = True

    def info(self, msg, *args: Any, **kwargs: Any):
        if not self.warning_printed:
            print('WARNING: EL LOGGER NO ESTA CONFIGURADO')
            self.warning_printed = True

    def warning(self, msg, *args: Any, **kwargs: Any):
        if not self.warning_printed:
            print('WARNING: EL LOGGER NO ESTA CONFIGURADO')
            self.warning_printed = True

    def error(self, msg, *args: Any, **kwargs: Any):
        if not self.warning_printed:
            print('WARNING: EL LOGGER NO ESTA CONFIGURADO')
            self.warning_printed = True

    def critical(self, msg, *args: Any, **kwargs: Any):
        if not self.warning_printed:
            print('WARNING: EL LOGGER NO ESTA CONFIGURADO')
            self.warning_printed = True
