import pytest

from ticketeer.repository.impl.sqlalchemy_user_repository import SQLAlchemyUserRepository

@pytest.fixture(scope='function')
def mock_sqlalchemy(mocker):
    return mocker.Mock()

@pytest.fixture(scope='function')
def user_repo(mock_sqlalchemy):
    repo = SQLAlchemyUserRepository(mock_sqlalchemy)
    yield repo

