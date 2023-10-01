class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class Configuration:
    def __init__(self, config = {}):
        self.config = config

    def set(self, key, value):
        self.config[key] = value

    def get(self, key):
        return self.config[key]
    

class SingletonConfiguration(Configuration, metaclass=Singleton):
    pass