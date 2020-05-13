class Config(object):
    """Parent class to inherit from. 
    These attributes are prod by default, and overriden by dev and testing configs. 
    """
    DEBUG = False
    TESTING = False

    # Check out the python secrets library
    SECRET_KEY = "pEY6ar2hZO7FsKBKgIUv"

    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "lowsecpass"

    # a nonfunctional example
    UPLOADS_DIR = "home/username/app/app/static/images/uploads"

    # will only send cookies back and forth if there's a secure https connection
    SESSOIN_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "lowsecpass"

    UPLOADS_DIR = "home/username/projects/flask_test/app/app/static/images/uploads"

    SESSOIN_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "lowsecpass"

    UPLOADS_DIR = "home/username/projects/flask_test/app/app/static/images/uploads"

    SESSOIN_COOKIE_SECURE = False