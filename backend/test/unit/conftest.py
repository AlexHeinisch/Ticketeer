import pytest
from ticketeer.dto.dtos import UserRole
from werkzeug.security import generate_password_hash
from ticketeer.models import User

@pytest.fixture(scope='session')
def sample_user_password():
    return 'hello123'

@pytest.fixture(scope='session')
def sample_user_password_hash(sample_user_password):
    return generate_password_hash(sample_user_password)

@pytest.fixture(scope='function')
def sample_user(sample_user_password_hash):
    usr: User = User(
        id = 1,
        username='Alex', 
        password_hash=sample_user_password_hash,
        email='test@example.com',
        role=UserRole.USER
    )
    return usr
