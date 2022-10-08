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

@pytest.fixture(scope='session')
def sample_user_base(sample_user_password_hash):
    usr: User = User(
        id = 1,
        username='Alex', 
        password_hash=sample_user_password_hash,
        email='test@example.com',
        role=UserRole.USER
    )
    return usr

@pytest.fixture(scope='function')
def sample_user(sample_user_base):
    return User.create_copy(sample_user_base)

@pytest.fixture(scope='session')
def sample_user2_password():
    return 'hello12345'

@pytest.fixture(scope='session')
def sample_user2_password_hash(sample_user2_password):
    return generate_password_hash(sample_user2_password)

@pytest.fixture(scope='session')
def sample_user2_base(sample_user2_password_hash):
    usr: User = User(
        id = 3,
        username='Alexandria', 
        password_hash=sample_user2_password_hash,
        email='alexa@example.com',
        role=UserRole.USER
    )
    return usr

@pytest.fixture(scope='function')
def sample_user2(sample_user2_base):
    return User.create_copy(sample_user2_base)

@pytest.fixture(scope='session')
def sample_admin_password():
    return 'somepass123'

@pytest.fixture(scope='session')
def sample_admin_password_hash(sample_admin_password):
    return generate_password_hash(sample_admin_password)

@pytest.fixture(scope='session')
def sample_admin_base(sample_admin_password_hash):
    usr: User = User(
        id = 2,
        username='Oleg', 
        password_hash=sample_admin_password_hash,
        email='admin@example.com',
        role=UserRole.ADMIN
    )
    return usr

@pytest.fixture(scope='function')
def sample_admin(sample_admin_base):
    return User.create_copy(sample_admin_base)
