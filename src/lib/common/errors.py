class ConnectionMaxRetriesException(Exception):
    def __init__(self):
        super().__init__("Couldn't stablish the connection. Maximum retries reached.")

class ReceivingTimeOut(Exception):
    def __init__(self):
        super().__init__("Receiving time out.")

class FileDoesNotExist(Exception):
    def __init__(self):
        super().__init__("File does not exist.")

class FileAlreadyExists(Exception):
    def __init__(self):
        super().__init__("File already exists.")
