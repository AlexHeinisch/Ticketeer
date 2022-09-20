from abc import ABC, abstractmethod
from ..dto.models import User, UserSearchRequest, UserUpdateRequest
from typing import NoReturn

class UserRepository(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_user_by_name(self, name: str) -> User:
        ...

    @abstractmethod
    def delete_user_by_name(self, name: str) -> NoReturn:
        ...

    @abstractmethod
    def insert_user(self, usr: User) -> User:
        ...

    @abstractmethod
    def get_users_by_search_req(self, req: UserSearchRequest) -> list[User]:
        ...

    @abstractmethod
    def update_user(self, req: UserUpdateRequest) -> User:
        ...
