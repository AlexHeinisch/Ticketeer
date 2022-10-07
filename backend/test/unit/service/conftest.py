import pytest

from ticketeer.service.impl.user_service_impl import UserServiceImpl


@pytest.fixture(scope='function')
def mock_repository(mocker):
    return mocker.Mock()

@pytest.fixture(scope='function')
def user_service(mock_repository):
    service = UserServiceImpl(mock_repository) 
    yield service

