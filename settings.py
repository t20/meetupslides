class Config(object):
    """Default config"""
    DEBUG = True

    APP_SECRET_KEY = '\x01\xd2+\x1c\x9b>\xdf\x85\xe65z\xba\xaa\x89\xfc\x18\xa4D\xb3\xe2\xa8\x1fP\x8d'
    
    REDIS_DB = 0
    REDIS_PORT = 6379
    REDIS_HOST = 'localhost'
    
    UPLOAD_FOLDER = '/tmp/'
    AWS_KEY = 'AKIAILGFFUGZMMIMHHHA'
    AWS_SECRET_KEY = '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'
    BUCKET_NAME = 'slides_dev'
    LOGOS_BUCKET_NAME = 'meetupslides_logos'

    MAIL_DEBUG = False
    
    r = None    

class ProductionConfig(Config):
    DEBUG = False

    APP_SECRET_KEY = ''


