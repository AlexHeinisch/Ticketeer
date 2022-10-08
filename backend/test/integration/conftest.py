import pytest
from ticketeer import create_app
from injector import Binder, singleton
from flask_sqlalchemy import SQLAlchemy
from ticketeer.config import TestingConfig
from ticketeer.repository.impl.sqlalchemy_user_repository import SQLAlchemyUserRepository
from ticketeer.repository.ticket_repository import TicketRepository
from ticketeer.repository.user_repository import UserRepository
from ticketeer.service.impl.ticket_service_impl import TicketServiceImpl
from ticketeer.service.impl.user_service_impl import UserServiceImpl
from ticketeer import db

from ticketeer.service.ticket_service import TicketService
from ticketeer.service.user_service import UserService

@pytest.fixture(scope='function')
def mock_user_service(mocker):
    return mocker.Mock()

@pytest.fixture(scope='function')
def mock_user_repo(mocker):
    return mocker.Mock()

@pytest.fixture(scope='function')
def mock_ticket_service(mocker):
    return mocker.Mock()

@pytest.fixture(scope='function')
def mock_ticket_repo(mocker):
    return mocker.Mock()

@pytest.fixture(scope='function')
def mock_sqlalchemy(mocker):
    return mocker.Mock()

@pytest.fixture(scope='function')
def level1_app(
        mock_user_service,
        mock_ticket_service
    ):
    
    def configure(binder: Binder):
        binder.bind(SQLAlchemy, to=None, scope=singleton)
        binder.bind(TicketService, to=mock_ticket_service, scope=singleton)
        binder.bind(UserService, to=mock_user_service, scope=singleton)
        binder.bind(UserRepository, to=None, scope=singleton)

    app = create_app({'SQLALCHEMY_DATABASE_URI': 'sqlite://'}, injector_module=configure)

    yield app

@pytest.fixture(scope='function')
def level1_client(level1_app):
    return level1_app.test_client()

@pytest.fixture(scope='function')
def level2_app(
    mock_user_repo,
    mock_ticket_repo
    ):
    
    def configure(binder: Binder):
        binder.bind(SQLAlchemy, to=None, scope=singleton)
        binder.bind(TicketService, to=TicketServiceImpl, scope=singleton)
        binder.bind(TicketRepository, to=mock_ticket_repo)
        binder.bind(UserService, to=UserServiceImpl, scope=singleton)
        binder.bind(UserRepository, to=mock_user_repo, scope=singleton)

    app = create_app({'SQLALCHEMY_DATABASE_URI': 'sqlite://'}, injector_module=configure)

    yield app

@pytest.fixture(scope='function')
def level2_client(level2_app):
    return level2_app.test_client()

@pytest.fixture(scope='function')
def level3_app(
    mock_sqlalchemy
    ):

    def configure(binder: Binder):
        binder.bind(SQLAlchemy, to=mock_sqlalchemy, scope=singleton)
        binder.bind(TicketService, to=TicketServiceImpl, scope=singleton)
        binder.bind(UserService, to=UserServiceImpl, scope=singleton)
        binder.bind(UserRepository, to=SQLAlchemyUserRepository, scope=singleton)

    app = create_app({'SQLALCHEMY_DATABASE_URI': 'sqlite://'}, injector_module=configure)

    yield app

@pytest.fixture(scope='function')
def level3_client(level3_app):
    return level3_app.test_client()

@pytest.fixture(scope='function')
def level4_app():
    def configure(binder: Binder):
        binder.bind(SQLAlchemy, to=db, scope=singleton)
        binder.bind(TicketService, to=TicketServiceImpl, scope=singleton)
        binder.bind(UserService, to=UserServiceImpl, scope=singleton)
        binder.bind(UserRepository, to=SQLAlchemyUserRepository, scope=singleton)

    app = create_app({'SQLALCHEMY_DATABASE_URI': 'sqlite://'}, injector_module=configure)

    yield app

@pytest.fixture(scope='function')
def level4_client(level4_app):
    return level4_app.test_client()
