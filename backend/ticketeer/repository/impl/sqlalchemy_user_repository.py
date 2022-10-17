import logging
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.exc
from injector import inject

from ticketeer.repository.user_repository import UserRepository
from ticketeer.dto.dtos import UserDto, UserRegisterRequestDto, UserSearchRequestDto, UserUpdateRequestDto
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
            return User.to_dto(usr[0])
        except sqlalchemy.exc.NoResultFound:
            return None

    def get_user_by_name(self, name: str) -> UserDto | None:
        self._logger.debug(f'[persistence] get_user_by_name: name={name}')
        try:
            usr = self._db.session.execute(self._db.select(User).filter_by(username=name)).one()
            return User.to_dto(usr[0])
        except sqlalchemy.exc.NoResultFound:
            return None
    
    def get_users_by_search_req(self, req: UserSearchRequestDto) -> list[UserDto]:
        self._logger.error(f'[persistence] get_users_by_search_req: req={req}')
        query = self._db.select(User)
        if req.email:
            query = query.filter(User.email.contains(req.email))
        if req.username:
            query = query.filter(User.username.contains(req.username))
        if req.role:
            query = query.filter(User.role == req.role)
        query = query.limit(req.num).offset(req.offset)
        try:
            usrs = self._db.session.execute(query).all()
            return [User.to_dto(u[0]) for u in usrs]
        except sqlalchemy.exc.NoResultFound:
            return []

    def insert_user(self, dto: UserRegisterRequestDto) -> UserDto:
        self._logger.debug(f'[persistence] insert_user: dto={dto}')
        usr: User = User(username=dto.username, password_hash=dto.password, email=dto.email)
        usr.id = None
        self._db.session.add(usr)
        self._db.session.commit()
        return User.to_dto(usr)

    def delete_user_by_name(self, name: str) -> None:
        self._logger.debug(f'[persistence] delete_user_by_name: name={name}')
        usr = self._db.session.execute(self._db.select(User).filter_by(username=name)).one()
        self._db.session.delete(usr[0])
        self._db.session.commit()
        
    def delete_user_by_id(self, id: int) -> None:
        self._logger.debug(f'[persistence] delete_user_by_id: id={id}')
        usr = self._db.session.execute(self._db.select(User).filter_by(id=id)).one()
        self._db.session.delete(usr[0])
        self._db.session.commit()

    def update_user(self, req: UserUpdateRequestDto) -> UserDto:
        self._logger.error(f'[persistence] update_user: req={req}')
        usr = self._db.session.execute(self._db.select(User).filter_by(id=req.id)).one()
        usr = usr[0]
        if req.username:
            usr.username = req.username
        if req.new_password:
            usr.password_hash = req.new_password
        if req.email:
            usr.email = req.email
        if req.role:
            usr.role = req.role
        self._db.session.commit()
        return User.to_dto(usr)
