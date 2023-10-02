class FTPServer():
    def __init__(self):
        self.file_name = None
        

    def handle_new_message(self, opt, payload):
        if opt == 'METADATA':
            self.handle_metadata(payload)
        elif opt == 'DATA':
            self.handle_data(payload)
        else:
            print(f'Unknown operation type {opt}')

    def handle_metadata(self, payload: bytes):
        file_name = payload.decode('utf-8')
        self.file_name = 'store/' + file_name
    
    def handle_data(self, payload: bytes):
        with open(self.file_name, 'ab') as f:
            f.write(payload)
