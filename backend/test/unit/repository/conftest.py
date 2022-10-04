import pytest
from ticketeer.dto.dtos import UserRole

from ticketeer.repository.impl.sqlalchemy_user_repository import SQLAlchemyUserRepository, User


@pytest.fixture(scope='session')
def sample_user():
    usr: User = User(
        id = 1,
        username='Alex', 
        password_hash='hello123', 
        email='test@example.com',
        role=UserRole.USER
    )
    return usr

@pytest.fixture(scope='function')
def mock_sqlalchemy(mocker):
    return mocker.Mock()

@pytest.fixture(scope='function')
def user_repo(mock_sqlalchemy):
    repo = SQLAlchemyUserRepository(mock_sqlalchemy)
    yield repo

