import logging
from typing import NoReturn
from injector import inject
from flask import g

from ticketeer.error.custom_errors import ConflictError, NotFoundError, PermissionError

from ticketeer.repository.user_repository import UserRepository

from ticketeer.dto.dtos import UserDto, UserRegisterRequestDto, UserRole, LoginRequestDto, UserSearchRequestDto, UserUpdateRequestDto

from werkzeug.security import generate_password_hash, check_password_hash
from ticketeer.service.user_service import UserService

class UserServiceImpl(UserService):

    @inject
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository
        self._logger = logging.getLogger(__name__)


    def verify_login(self, req: LoginRequestDto) -> bool:
        usr = self._repository.get_user_by_name(req.username)
        if usr:
            return check_password_hash(usr.password_hash, req.password)

        return False

    def _verify_login_by_id(self, id, password):
        usr = self._repository.get_user_by_id(id)
        if usr:
            return self.verify_login(LoginRequestDto(username=usr.username, password=password))
        return False

    def get_user_by_id(self, id: int) -> UserDto:
        usr = self._repository.get_user_by_id(id)
        if usr:
            return usr
        else:
            raise NotFoundError(f'Could not find user with id \'{id}\'')

    def get_user_by_name(self, name: str) -> UserDto:
        usr = self._repository.get_user_by_name(name)
        if usr:
            return usr
        else:
            raise NotFoundError(f'Could not find user with name \'{name}\'')

    def get_multiple_users(self, req: UserSearchRequestDto) -> list[UserDto]:
        return self._repository.get_users_by_search_req(req)


    def register_user(self, req: UserRegisterRequestDto) -> UserDto:
        if self._repository.get_user_by_name(req.username):
            raise ConflictError('username already in use')

        # replace password with hash to be stored in database
        req.password = generate_password_hash(req.password)

        return self._repository.insert_user(req)


    def delete_user_by_name(self, name: str) -> None:
        if (not name == g.user) and g.role is not UserRole.ADMIN:
            raise PermissionError('forbidden')

        if not self._repository.get_user_by_name(name):
            raise NotFoundError('given user does not exist')

        self._repository.delete_user_by_name(name)


    def delete_user_by_id(self, id: int) -> None:
        #if (not id == g.id) and g.role is not UserRole.ADMIN:
        #    raise PermissionError('forbidden')

        if not self._repository.get_user_by_id(id):
            raise NotFoundError('given user does not exist')

        self._repository.delete_user_by_id(id)


    def update_user(self, req: UserUpdateRequestDto) -> UserDto:
        if (not req.username == g.user) and g.role is not UserRole.ADMIN:
            raise PermissionError('forbidden')

        if not self._repository.get_user_by_id(req.id):
            raise NotFoundError('given user does not exist')
        #if req.icon_id and not self._icon_service.icon_exists(req.icon_id):
        #    raise ConflictError(f'icon with id {req.icon_id} does not exist!')    
        if req.role and g.role is not UserRole.ADMIN:
            raise PermissionError('forbidden')
        if req.new_password and not req.old_password:
            raise ConflictError('old_password needs to be provided to set the new one')
        if req.new_password and not self._verify_login_by_id(req.id,req.old_password):
            raise PermissionError('could not authenticate')
        if req.new_password:
            req.new_password = generate_password_hash(req.new_password)
        return self._repository.update_user(req)
