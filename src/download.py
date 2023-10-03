from lib.common.file_handler import FileHandler
from lib.common.message import Message

from lib.helpers.network_builder import NetworkBuilder
from lib.common.parser import parse_download_args
from lib.common.logger_setup import logger_setup
from lib.constants import DEFAULT_MESSAGE_SIZE

def calculate_file_size_in_packets(file_size):
    return file_size / (DEFAULT_MESSAGE_SIZE) + 1

def calculate_percentage(packets_received, file_size):
    return (packets_received / calculate_file_size_in_packets(file_size)) * 100

def download(parsed_args):
    logger = logger_setup(parsed_args)

    client = NetworkBuilder('CLIENT')\
        .set_logger(logger)\
        .set_host(parsed_args.host)\
        .set_port(parsed_args.port)\
        .set_protocol(parsed_args.protocol)\
        .build()

    try:
        logger.info("Client download started")
        client.connect()
        client.send(Message.build_metadata_payload(parsed_args.name, 'download'))
        file_handler = FileHandler('downloads/' + parsed_args.name)
        file_size = 0
        packets_received = 0
        while True:
            data = client.recv()
            opt = Message.unwrap_operation_type(data)
            if opt == 'METADATA':
                payload = Message.unwrap_payload_metadata(data)
                if payload == b'ERROR_FILE_DOES_NOT_EXIST':
                    logger.error("File does not exist")
                    break
                else :
                    file_size = int(payload)
                    logger.info('Will receive {0} bytes'.format(file_size) )
            else:
                payload = Message.unwrap_payload_data(data)
                packets_received += 1
                if(packets_received % min(100, calculate_file_size_in_packets(file_size) // 2) == 0):
                    logger.info('Received {0:.2f} % '.format(calculate_percentage(packets_received, file_size)))
                if payload == b'exit':
                    logger.info('Download completed')
                    #client.close()
                    break
                file_handler.write_bytes(payload)
    except KeyboardInterrupt:
        logger.info("Client download stopped by user")
        exit(0)
    except Exception:
        logger.error("Client upload stopped unexpectedly")



if __name__ == "__main__":
    parsed_args = parse_download_args()
    download(parsed_args)
