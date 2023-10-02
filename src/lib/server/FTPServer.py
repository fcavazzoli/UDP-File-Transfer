class FTPServer():
    def __init__(self) -> None:
        self.file_name = None
        pass

    def handle_new_message(self, opt, payload):
        if opt == 'METADATA':
            self.handle_metadata(payload)
        elif opt == 'DATA':
            self.handle_data(payload)
        elif opt == 'EXIT':
            self.handle_exit(payload)
        else:
            print(f'Unknown operation type {opt}')

    def handle_metadata(self, payload: bytes):
        self.file_name = payload.decode('utf-8')
    
    def handle_data(self, payload: bytes):
        with open(self.file_name, 'ab') as f:
            f.write(payload)
    
    def handle_exit(self, payload: bytes):
        print('Exiting...')
        