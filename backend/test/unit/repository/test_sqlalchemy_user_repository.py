from ticketeer.dto.dtos import UserRegisterRequestDto, UserRole
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

