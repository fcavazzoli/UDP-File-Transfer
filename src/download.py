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

def download(parsed_args, first_download):
    logger = logger_setup(parsed_args)

    if not first_download:
        # Prompt the user for a new file name, but only if it's not the first download
        name = input("Enter the name of the file you want to download: ").strip()
    else:
        # Use the provided file name for the first download
        name = parsed_args.name

    client = NetworkBuilder('CLIENT')\
        .set_logger(logger)\
        .set_host(parsed_args.host)\
        .set_port(parsed_args.port)\
        .set_protocol(parsed_args.protocol)\
        .build()

    try:
        logger.info("Client download started")
        client.connect()
        client.send(Message.build_metadata_payload(name, 'download'))
        file_handler = FileHandler('downloads/' + name)
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
                    client.close()
                    break
                file_handler.write_bytes(payload)
    except KeyboardInterrupt:
        logger.info("Client download stopped by user")
        client.close()
        exit(0)
    except Exception as e:
        logger.error("Client download stopped unexpectedly with error: " + str(e))
        client.close()


if __name__ == "__main__":
    first_download = True  # Initialize the flag for the first download
    while True:  # Continue downloading files until the user decides to exit
        parsed_args = parse_download_args()
        download(parsed_args, first_download)
        first_download = False  # Set the flag to False after the first download

        # Ask the user if they want to download another file
        while True:
            another_download = input("Do you want to download another file? (yes/no): ").strip().lower()
            if another_download == "yes" or another_download == "no":
                break  # Exit the inner loop if the user enters "yes" or "no"
            else:
                print("Please enter 'yes' or 'no'.")  # Reprompt for a valid input

        if another_download != "yes":
            break  # Exit the outer loop if the user doesn't want to download another file