from default_config import Config
from app import app

class Production(Config):
    PRODUCTION = True
    SQLALCHEMY_DATABASE_URI = "postgresql://secondlife@192.168.0.127/secondlife"

class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://felix@192.168.0.127/secondlife"

class Testing(Config):
    TESTING = True
