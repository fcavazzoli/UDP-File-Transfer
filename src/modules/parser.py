import argparse

def build_base_parser(command_desc):
    """Contruye el parser con los argumentos comunes a todos los comandos: download, upload y start-server"""

    parser = argparse.ArgumentParser(description=command_desc)

    #TODO: Poner un valor default de ip, de puerto y protocolo, para no tener que ir escribiendo siempre

    # resumen argparse: https://realpython.com/command-line-interfaces-python-argparse
    #   store_true = guardar True si se encuentra el argumento, False de lo contrario
    #   store = guarda el valor del argumento, si la flag no esta, guarda None
    #   metavar = nombre del argumento que se muestra en el help

    # solo permite o verbose o quiet, no ambas
    group = parser.add_mutually_exclusive_group()
    group.add_argument( "-v", "--verbose", action="store_true", help="increase output verbosity")
    group.add_argument( "-q", "--quiet", action="store_true", help="decrease output verbosity")

    parser.add_argument("-H", "--host", action="store", metavar="addr", help="server IP address")
    parser.add_argument("-p", "--port", action="store", metavar="port", help="server port")

    # Tipo de protocolo: Stop and Wait o Selective Repeat
    # Es un nuevo argumento, no está explicitamente en el enunciado
    parser.add_argument("-P", "--protocol", metavar="protocol", help="server/client protocol")

    return parser

def parse_download_args():
    """Parsea los argumentos para el comando download y devuelve un objeto con los argumentos parseados"""
    parser = build_base_parser("Downloads a file from a server")
    parser.add_argument("-d", "--dst", action="store", metavar="filepath", help="destination file path")
    parser.add_argument("-n", "--name", action="store", metavar="filename", help="file name") #, required=True)

    parsed_args = parser.parse_args()
    return parsed_args


def parse_upload_args():
    """Parsea los argumentos para el comando upload y devuelve un objeto con los argumentos parseados"""
    parser = build_base_parser("Uploads a file to a server")
    parser.add_argument("-s", "--src", action="store", metavar="filepath", help="source file path")
    parser.add_argument("-n", "--name", action="store", metavar="filename", help="file name") #, required=True)
    # NOTE: poner un nombre default al archivo o ponerlo siempre como requerido?

    parsed_args = parser.parse_args()
    return parsed_args

def parse_server_args():
    """Parsea los argumentos para el comando start-server y devuelve un objeto con los argumentos parseados"""
    parser = build_base_parser("Starts a server that accepts file uploads and downloads")
    parser.add_argument("-s", "--storage", action="store", metavar="dirpath", help="storage dir path")

    parsed_args = parser.parse_args()
    return parsed_args