class Config(object):
    """Default config"""
    DEBUG = True

    APP_SECRET_KEY = ''
    
    REDIS_DB = 0
    REDIS_PORT = 6379
    REDIS_HOST = 'localhost'
    
    r = None    

class ProductionConfig(Config):
    DEBUG = False

    APP_SECRET_KEY = ''


