import os
import pytz
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TEMPLATE_AUTO_RELOAD = True
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = 'postgresql://taxi:taxi@localhost/taxidb'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    LANGUAGES = {
        'en': 'English',
        'sk': 'Slovensky'
    }
    UTC_TIMEZONE = pytz.timezone('UTC')
    LOCAL_TIMEZONE = pytz.timezone('Europe/Bratislava')


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://taxi:taxi@localhost/taxidb'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class TestingConfig(Config):
    TESTING = True
