import pytest
from ticketeer import create_app
from injector import Binder

@pytest.fixture(scope='function')
def app():
    
    def configure(binder: Binder): 
        ... # put mocked-stuff that can't be tested in here

    app = create_app({'SQLALCHEMY_DATABASE_URI': 'sqlite://'}, injector_module=configure)

    yield app

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()
