from abc import ABC, abstractmethod
from ..models import User, UserSearchRequest, UserUpdateRequest

class TicketDao(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def get(self):
        pass

class UserDao(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_user_by_name(self, name) -> User | None:
        pass

    @abstractmethod
    def delete_user_by_name(self, name: str) -> None:
        pass

    @abstractmethod
    def insert_user(usr: User) -> User:
        pass

    @abstractmethod
    def get_users_by_search_req(self, req: UserSearchRequest) -> list[User]:
        pass

    @abstractmethod
    def update_user(self, req: UserUpdateRequest) -> User:
        pass