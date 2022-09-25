import logging
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.exc
from injector import inject

from ticketeer.repository.user_repository import UserRepository
from ticketeer.dto.dtos import UserDto, UserSearchRequestDto, UserUpdateRequestDto
from ticketeer.models import User

class SQLAlchemyUserRepository(UserRepository):

    @inject
    def __init__(self, db: SQLAlchemy) -> None:
        super().__init__()
        self._db = db
        self._logger = logging.getLogger(__name__)

    def get_user_by_id(self, id: int) -> UserDto | None:
        self._logger.debug(f'[persistence] get_user_by_id: id={id}')
        try:
            usr = self._db.session.execute(self._db.select(User).filter_by(id=id)).one()
            return usr.to_dto()
        except sqlalchemy.exc.NoResultFound:
            return None

    def get_user_by_name(self, name: str) -> UserDto | None:
        self._logger.debug(f'[persistence] get_user_by_name: name={name}')
        try:
            usr = self._db.session.execute(self._db.select(User).filter_by(username=name)).one()
            return usr.to_dto()
        except sqlalchemy.exc.NoResultFound:
            return None
    
    def get_users_by_search_req(self, req: UserSearchRequestDto) -> list[UserDto]:
        self._logger.error(f'[persistence] get_users_by_search_req: req={req}')
        return []

    def insert_user(self, usr_dto: UserDto) -> UserDto:
        self._logger.debug(f'[persistence] insert_user: usr_dto={usr_dto}')
        usr: User = User(username=usr_dto.username, password_hash='dasd', email='sdaasdas')
        self._db.session.add(usr)
        self._db.session.commit()
        return usr.to_dto()

    def delete_user_by_name(self, name: str) -> None:
        self._logger.debug(f'[persistence] delete_user_by_name: name={name}')
        usr = self._db.session.query(User).get(name)
        self._db.session.delete(usr)
        self._db.session.commit()
        pass

    def update_user(self, req: UserUpdateRequestDto) -> UserDto:
        self._logger.error(f'[persistence] update_user: req={req}')
        return UserDto(id=0, username='bob', password='Bob', email='bob')
