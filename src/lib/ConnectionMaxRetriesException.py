class ConnectionMaxRetriesException(Exception):
    def __init__(self):
        super().__init__("Couldn't stablish the connection. Maximum retries reached.")
