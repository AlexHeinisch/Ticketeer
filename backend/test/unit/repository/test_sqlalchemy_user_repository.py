from ticketeer.dto.dtos import UserRegisterRequestDto, UserRole, UserUpdateRequestDto
from ticketeer.models import User
from ticketeer.repository.impl.sqlalchemy_user_repository import SQLAlchemyUserRepository

def test_get_user_by_name(
    sample_user: User,
    user_repo: SQLAlchemyUserRepository,
    mock_sqlalchemy
    ):
    mock_sqlalchemy.session.execute.return_value.one.return_value = sample_user
    assert sample_user.to_dto() == user_repo.get_user_by_name(sample_user.username)
    mock_sqlalchemy.select.return_value.filter_by.assert_called_once_with(username=sample_user.username)

def test_get_user_by_id(
    sample_user: User,
    user_repo: SQLAlchemyUserRepository,
    mock_sqlalchemy
    ):
    mock_sqlalchemy.session.execute.return_value.one.return_value = sample_user
    assert sample_user.to_dto() == user_repo.get_user_by_id(sample_user.id)
    mock_sqlalchemy.select.return_value.filter_by.assert_called_once_with(id=sample_user.id)

def test_insert_user(
    sample_user: User,
    user_repo: SQLAlchemyUserRepository,
    mock_sqlalchemy
    ):
    user_repo.insert_user(UserRegisterRequestDto(username=sample_user.username,
                                                 password=sample_user.password_hash,
                                                 email=sample_user.email))
    sample_user.id= -1
    sample_user.role = UserRole.USER
    mock_sqlalchemy.session.add.assert_called_once_with(sample_user)
    mock_sqlalchemy.session.commit.assert_called_once()

def test_delete_user_by_name(
    sample_user: User,
    user_repo: SQLAlchemyUserRepository,
    mock_sqlalchemy
    ):
    mock_sqlalchemy.session.execute.return_value.one.return_value = sample_user
    user_repo.delete_user_by_name(sample_user.username)

    mock_sqlalchemy.select.return_value.filter_by.assert_called_once_with(username=sample_user.username)
    mock_sqlalchemy.session.delete.assert_called_once_with(sample_user)
    mock_sqlalchemy.session.commit.assert_called_once()


def test_delete_user_by_id(
    sample_user: User,
    user_repo: SQLAlchemyUserRepository,
    mock_sqlalchemy
    ):
    mock_sqlalchemy.session.execute.return_value.one.return_value = sample_user
    user_repo.delete_user_by_id(sample_user.id)

    mock_sqlalchemy.select.return_value.filter_by.assert_called_once_with(id=sample_user.id)
    mock_sqlalchemy.session.delete.assert_called_once_with(sample_user)
    mock_sqlalchemy.session.commit.assert_called_once()

def test_update_user_name(
    sample_user: User,
    user_repo: SQLAlchemyUserRepository,
    mock_sqlalchemy
    ):
    expected_user = User(username='newusername', email=sample_user.email, password_hash=sample_user.password_hash, id=sample_user.id, role=sample_user.role)
    mock_sqlalchemy.session.execute.return_value.one.return_value = sample_user
    returned_usr = user_repo.update_user(UserUpdateRequestDto(sample_user.id, username=expected_user.username))
    assert returned_usr == expected_user.to_dto()
    mock_sqlalchemy.session.commit.assert_called_once()
    

def test_update_user_email(
    sample_user: User,
    user_repo: SQLAlchemyUserRepository,
    mock_sqlalchemy
    ):
    expected_user = User(username=sample_user.username, email='test@example.com', password_hash=sample_user.password_hash, id=sample_user.id, role=sample_user.role)
    mock_sqlalchemy.session.execute.return_value.one.return_value = sample_user
    returned_usr = user_repo.update_user(UserUpdateRequestDto(sample_user.id, email='test@example.com'))
    assert returned_usr == expected_user.to_dto()
    mock_sqlalchemy.session.commit.assert_called_once()

def test_update_user_password(
    sample_user: User,
    user_repo: SQLAlchemyUserRepository,
    mock_sqlalchemy
    ):
    expected_user = User(username=sample_user.username, email=sample_user.email, password_hash='hash123', id=sample_user.id, role=sample_user.role)
    mock_sqlalchemy.session.execute.return_value.one.return_value = sample_user
    returned_usr = user_repo.update_user(UserUpdateRequestDto(sample_user.id, new_password='hash123'))
    assert returned_usr == expected_user.to_dto()

def test_update_user_role(
    sample_user: User,
    user_repo: SQLAlchemyUserRepository,
    mock_sqlalchemy
    ):
    expected_user = User(username=sample_user.username, email=sample_user.email, password_hash=sample_user.password_hash, id=sample_user.id, role=UserRole.ADMIN)
    mock_sqlalchemy.session.execute.return_value.one.return_value = sample_user
    returned_usr = user_repo.update_user(UserUpdateRequestDto(sample_user.id, role=UserRole.ADMIN))
    assert returned_usr == expected_user.to_dto()
    mock_sqlalchemy.session.commit.assert_called_once()

def test_update_user_all(
    sample_user: User,
    user_repo: SQLAlchemyUserRepository,
    mock_sqlalchemy
    ):
    expected_user = User(username='user123', email='email@example.com', password_hash='hash123', id=sample_user.id, role=UserRole.ADMIN)
    mock_sqlalchemy.session.execute.return_value.one.return_value = sample_user
    returned_usr = user_repo.update_user(UserUpdateRequestDto(sample_user.id, username='user123', email='email@example.com', new_password='hash123', role=UserRole.ADMIN))
    assert returned_usr == expected_user.to_dto()
    mock_sqlalchemy.session.commit.assert_called_once()

