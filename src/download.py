from modules.parser import parse_download_args


if __name__ == "__main__":
    parsed_args = parse_download_args()
    
    print(parsed_args)
    print(parsed_args.host)
    print(parsed_args.verbose)
    
    #TODO: logger
    #TODO: seleccionar protocolo
    #TODO: descargar (?