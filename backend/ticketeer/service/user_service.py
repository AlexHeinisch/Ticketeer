import logging
from injector import inject
from flask import g

from ..error.custom_errors import ConflictError, NotFoundError, PermissionError

from ..repository.user_repository import UserRepository

from ..dto.models import User, UserRole, LoginRequest, UserSearchRequest, UserUpdateRequest

from werkzeug.security import generate_password_hash, check_password_hash

class UserService():

    @inject
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository
        self._logger = logging.getLogger(__name__)


    def verify_login(self, req: LoginRequest) -> bool:
        usr = self._repository.get_user_by_name(req.username)
        if usr:
            return check_password_hash(usr.password, req.password)

        return False


    def get_single_user(self, name: str) -> User:
        user = self._repository.get_user_by_name(name)

        if not user:
            raise NotFoundError('given user does not exist')

        return user


    def get_multiple_users(self, req: UserSearchRequest) -> list[User]:
        return self._repository.get_users_by_search_req(req)


    def register_user(self, usr: User) -> User:
        if self._repository.get_user_by_name(usr.username):
            raise ConflictError('username already in use')

        #if not self._icon_service.icon_exists(usr.icon_id):
        #    raise ConflictError(f'icon with id {usr.icon_id} does not exist!')

        usr.password = generate_password_hash(usr.password)
        usr.role = UserRole.USER

        return self._repository.insert_user(usr)


    def delete_user_by_name(self, name: str) -> None:
        if (not name == g.user) and g.role is not UserRole.ADMIN:
            raise PermissionError('forbidden')

        if not self._repository.get_user_by_name(name):
            raise NotFoundError('given user does not exist')

        self._repository.delete_user_by_name(name)

    def update_user(self, req: UserUpdateRequest) -> User:
        if (not req.username == g.user) and g.role is not UserRole.ADMIN:
            raise PermissionError('forbidden')

        if not self._repository.get_user_by_name(req.username):
            raise NotFoundError('given user does not exist')
        #if req.icon_id and not self._icon_service.icon_exists(req.icon_id):
        #    raise ConflictError(f'icon with id {req.icon_id} does not exist!')    
        if req.role and g.role is not UserRole.ADMIN:
            raise PermissionError('forbidden')
        if req.new_password and not req.old_password:
            raise ConflictError('old_password needs to be provided to set the new one')
        if req.new_password and not self.verify_login(LoginRequest(req.username, req.old_password)):
            raise PermissionError('could not authenticate')
        if req.new_password:
            req.new_password = generate_password_hash(req.new_password)
        return self._repository.update_user(req)
