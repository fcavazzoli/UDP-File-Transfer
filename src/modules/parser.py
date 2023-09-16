import argparse

def build_base_parser(command_desc):
    """Contruye el parser con los argumentos comunes a todos los comandos: download, upload y start-server"""

    parser = argparse.ArgumentParser(description=command_desc)

    #TODO: Poner un valor default de ip y de puerto, para no tener que ir escribiendo siempre

    # store_true = guardar True si se encuentra el argumento, False si no
    # metavar = pide un valor para el argumento y lo guarda bajo el nombre (largo) de la flag
    parser.add_argument( "-v", "--verbose", action="store_true", help="increase output verbosity")
    parser.add_argument( "-q", "--quiet", action="store_true", help="decrease output verbosity")
    parser.add_argument("-H", "--host", metavar="addr", help="server IP address")
    parser.add_argument("-p", "--port", metavar="port", help="server port")

    # NOTE: Es un nuevo argumento, no está explicitamente en el enunciado
    #Tipo de protocolo: Stop and Wait o Selective Repeat
    parser.add_argument("-P", "--prot", metavar="protocol", help="server/client protocol")

    return parser

def parse_download_args():
    """Parsea los argumentos para el comando download y devuelve un objeto con los argumentos parseados"""
    parser = build_base_parser("Downloads a file from a server")
    parser.add_argument("-d", "--dst", metavar="filepath", help="destination file path")
    parser.add_argument("-n", "--name", metavar="filename", help="file name")

    parsed_args = parser.parse_args()
    return parsed_args
