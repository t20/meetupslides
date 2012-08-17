class Config(object):
    """Default config"""
    DEBUG = True

    APP_SECRET_KEY = ''

    

class ProductionConfig(Config):
    DEBUG = False

    APP_SECRET_KEY = ''


