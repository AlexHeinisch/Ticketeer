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
