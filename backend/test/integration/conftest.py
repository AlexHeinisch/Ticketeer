import pytest
from ticketeer import create_app
from injector import Binder

from ticketeer.security.authentication import generate_token
from ticketeer import db

@pytest.fixture(scope='session')
def test_settings():
    return {
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'SECRET_KEY': 'TOP_SECRET'
    }

@pytest.fixture(scope='function')
def app(test_settings):
    
    def configure(binder: Binder): 
        ... # put mocked-stuff that can't be tested in here

    app = create_app(test_settings, injector_module=configure)

    yield app

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='session')
def sample_user_token(sample_user_base, test_settings):
    return generate_token(sample_user_base.id, sample_user_base.username, sample_user_base.role, test_settings['SECRET_KEY'])

@pytest.fixture(scope='session')
def sample_user2_token(sample_user2_base, test_settings):
    return generate_token(sample_user2_base.id, sample_user2_base.username, sample_user2_base.role, test_settings['SECRET_KEY'])

@pytest.fixture(scope='session')
def sample_admin_token(sample_admin_base, test_settings):
    return generate_token(sample_admin_base.id, sample_admin_base.username, sample_admin_base.role, test_settings['SECRET_KEY'])

