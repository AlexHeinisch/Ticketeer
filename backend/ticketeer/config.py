from os import environ, path
from dotenv import load_dotenv

basedir = path.dirname(path.dirname(path.abspath(__file__)))
load_dotenv(path.join(basedir, '.env'))

def load_config(mode=environ.get('MODE')):
    """Load config."""
    try:
        if mode == 'PRODUCTION':
            return ProductionConfig
        elif mode == 'TESTING':
            return TestingConfig
        else:
            return DevelopmentConfig
    except ImportError:
        return Config

class Config(object):
    """Base Config"""
    SECRET_KEY = environ.get('SECRET_KEY') or 'supersecret'
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir,'test.db')

class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False

