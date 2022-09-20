import logging
from ..user_repository import UserRepository
from flask_sqlalchemy import SQLAlchemy

from injector import inject

from ...dto.models import User, UserSearchRequest, UserUpdateRequest

class SQLAlchemyUserRepository(UserRepository):

    @inject
    def __init__(self, db: SQLAlchemy) -> None:
        super().__init__()
        self._db = db
        self._logger = logging.getLogger(__name__)

    def get_user_by_name(self, name: str) -> User:
        self._logger.debug(f'[persistence] get_user_by_name: name={name}')
        return User('xx', 'xx', 'xx')
    
    def get_users_by_search_req(self, req: UserSearchRequest) -> list[User]:
        self._logger.error(f'[persistence] get_users_by_search_req: req={req}')
        return []

    def insert_user(self, usr: User) -> User:
        self._logger.debug(f'[persistence] insert_user: usr={usr}')
        return User('xx', 'xx', 'xx')

    def delete_user_by_name(self, name: str) -> None:
        self._logger.debug(f'[persistence] delete_user_by_name: name={name}')
        pass

    def update_user(self, req: UserUpdateRequest) -> User:
        self._logger.error(f'[persistence] update_user: req={req}')
        return User('xx', 'xx', 'xx')
