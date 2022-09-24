from flask_sqlalchemy import SQLAlchemy
import pytest

from ....ticketeer.repository.impl.sqlalchemy_user_repository import SQLAlchemyUserRepository, User

@pytest.fixture(scope='session')
def sample_user():
    usr: User = User('Alex', 'hello123', 'test@example.com')
    yield usr

@pytest.fixture(scope='function')
def user_repo():
    alch: SQLAlchemy = SQLAlchemy()
    repo = SQLAlchemyUserRepository(alch)
    yield repo

