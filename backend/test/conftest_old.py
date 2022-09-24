from flask import Flask
import pytest
from scoutsticketservice.models import User, UserRole
from scoutsticketservice import create_app
from scoutsticketservice.security.authentication import generate_token
from scoutsticketservice.persistence.base_daos import TicketDao, UserDao
from scoutsticketservice.persistence.implementations.dummy_daos import DummyTicketDao, DummyUserDao
from injector import Binder, singleton

from werkzeug.security import generate_password_hash

SECRET_KEY = 'test'

@pytest.fixture(scope='session')
def app(injector_module):
    app = create_app({
        'DB_HOST': '127.0.0.1',
        'DB_DATABASE': 'postgres',
        'DB_USERNAME': 'postgres',
        'DB_PASSWORD': 'password',
        'SECRET_KEY': SECRET_KEY
    }, injector_module)
    app.config.update({
        "TESTING": True
    })

    yield app

@pytest.fixture(scope='session')
def injector_module(user_dao, ticket_dao):
    def test_configure(binder: Binder):
        binder.bind(UserDao, to=user_dao, scope=singleton)
        binder.bind(TicketDao, to=ticket_dao, scope=singleton)

    yield test_configure

@pytest.fixture(scope='session')
def user_dao():
    dao = DummyUserDao()
    yield dao

@pytest.fixture(scope='session')
def ticket_dao():
    dao = DummyTicketDao()
    yield dao

@pytest.fixture(scope='function')
def client(app: Flask):
    yield app.test_client()

## sample users

@pytest.fixture(scope='session')
def user1_base():
    usr = User('Max Mustermann', 'maxmustermann123', 'max.mustermann@example.com', -1, UserRole.USER)
    yield usr

@pytest.fixture(scope='function')
def user1(user1_base):
    yield user1_base.copy()

@pytest.fixture(scope='session')
def user1_hashed_pw(user1_base):
    yield generate_password_hash(user1_base.password)

@pytest.fixture(scope='session')
def valid_user1_token(user1_base):
    token = generate_token(user1_base.username, user1_base.role, SECRET_KEY)
    yield token

@pytest.fixture(scope='session')
def user2_base():
    usr = User('Stella Standard', 'stellastandard123', 'stella.standard@example.com', -1, UserRole.USER)
    yield usr

@pytest.fixture(scope='function')
def user2(user2_base):
    yield user2_base.copy()

@pytest.fixture(scope='session')
def user2_hashed_pw(user2_base):
    yield generate_password_hash(user2_base.password)

@pytest.fixture(scope='session')
def valid_user2_token(user2_base):
    token = generate_token(user2_base.username, user2_base.role, SECRET_KEY)
    yield token

@pytest.fixture(scope='session')
def admin1_base():
    usr = User('Admin Alex', 'adminalex123', 'admin.alex@example.com', -1, UserRole.ADMIN)
    yield usr

@pytest.fixture(scope='function')
def admin1(admin1_base):
    yield admin1_base.copy()

@pytest.fixture(scope='session')
def admin1_hashed_pw(admin1_base):
    yield generate_password_hash(admin1_base.password)

@pytest.fixture(scope='session')
def valid_admin1_token(admin1_base):
    token = generate_token(admin1_base.username, admin1_base.role, SECRET_KEY)
    yield token

@pytest.fixture(scope='session')
def admin2_base():
    usr = User('Operator Olaf', 'operatorolaf123', 'olaf.o@example.com', -1, UserRole.ADMIN)
    yield usr

@pytest.fixture(scope='function')
def admin2(admin2_base):
    yield admin2_base.copy()

@pytest.fixture(scope='session')
def admin2_hashed_pw(admin2_base):
    yield generate_password_hash(admin2_base.password)

@pytest.fixture(scope='session')
def valid_admin2_token(admin2_base):
    token = generate_token(admin2_base.username, admin2_base.role, SECRET_KEY)
    yield token

@pytest.fixture(scope='function')
def client_with_test_data(client, user_dao: DummyUserDao,
     ticket_dao: DummyTicketDao, 
     user1_base, user2_base, admin1_base, admin2_base,
     user1_hashed_pw, user2_hashed_pw, admin1_hashed_pw, admin2_hashed_pw):

    # insert test users (test_bottleneck)
    tmp_user1 = user1_base.copy(); tmp_user1.password = user1_hashed_pw
    user_dao.insert_user(tmp_user1)
    tmp_user2 = user2_base.copy(); tmp_user2.password = user2_hashed_pw
    user_dao.insert_user(tmp_user2)
    tmp_admin1 = admin1_base.copy(); tmp_admin1.password = admin1_hashed_pw
    user_dao.insert_user(tmp_admin1)
    tmp_admin2 = admin2_base.copy(); tmp_admin2.password = admin2_hashed_pw
    user_dao.insert_user(tmp_admin2)

    yield client

    user_dao._storage = {}
