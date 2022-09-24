import logging
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.exc
from injector import inject
from ticketeer.error.custom_errors import NotFoundError

from ticketeer.repository.user_repository import UserRepository
from ticketeer.dto.dtos import UserDto, UserSearchRequestDto, UserUpdateRequestDto
from ticketeer.models import User

class SQLAlchemyUserRepository(UserRepository):

    @inject
    def __init__(self, db: SQLAlchemy) -> None:
        super().__init__()
        self._db = db
        self._logger = logging.getLogger(__name__)

    def get_user_by_name(self, name: str) -> User:
        self._logger.debug(f'[persistence] get_user_by_name: name={name}')
        try:
            usr = self._db.session.execute(self._db.select(User).filter_by(username=name)).one()
        except sqlalchemy.exc.NoResultFound:
            raise NotFoundError(message=f'Could not find user with name \'{name}\'')
        return usr
    
    def get_users_by_search_req(self, req: UserSearchRequestDto) -> list[User]:
        self._logger.error(f'[persistence] get_users_by_search_req: req={req}')
        return []

    def insert_user(self, usr_dto: UserDto) -> User:
        self._logger.debug(f'[persistence] insert_user: usr_dto={usr_dto}')
        usr: User = User(username=usr_dto.username)
        self._db.session.add(usr)
        self._db.session.commit()
        return usr

    def delete_user_by_name(self, name: str) -> None:
        self._logger.debug(f'[persistence] delete_user_by_name: name={name}')
        usr = self._db.session.query(User).get(name)
        self._db.session.delete(usr)
        self._db.session.commit()
        pass

    def update_user(self, req: UserUpdateRequestDto) -> User:
        self._logger.error(f'[persistence] update_user: req={req}')
        return User('xx')
