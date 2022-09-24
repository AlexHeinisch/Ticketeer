from ....ticketeer.repository.impl.sqlalchemy_user_repository import SQLAlchemyUserRepository
from flask_sqlalchemy import SQLAlchemy
from ....ticketeer.dto.models import User
from unittest.mock import Mock

import flask_sqlalchemy

def test_x(sample_user: User, user_repo: SQLAlchemyUserRepository, mocker):
    mock_get = mocker.patch('ticketeer.repository.impl.sqlalchemy_user_repository._db.session.query.get', return_value = sample_user)
    mock_delete = mocker.patch('flask_sqlalchemy.SQLAlchemy.session.delete', return_value=None)
    mock_commit = mocker.patch('flask_sqlalchemy.SQLAlchemy.session.commit', return_value=None)
    user_repo.delete_user_by_name('Bob')

    mock_get.assert_called()
