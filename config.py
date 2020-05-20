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
    SESSION_COOKIE_SECURE = True

    # dummy public folder for download-access
    CLIENT_FILES = ""
    CLIENT_REPORTS = ""

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "lowsecpass"

    UPLOADS_DIR = "home/username/projects/flask_test/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = False
    CLIENT_FILES = "/Users/don/Documents/flask_jnash/app/static/client"
    CLIENT_REPORTS = "/Users/don/Documents/flask_jnash/app/static/client/reports"

class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "lowsecpass"

    UPLOADS_DIR = "home/username/projects/flask_test/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = False