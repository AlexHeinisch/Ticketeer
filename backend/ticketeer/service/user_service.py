from ..dto.models import User, LoginRequest, UserSearchRequest, UserUpdateRequest
from abc import ABC, abstractmethod

class UserService(ABC):

    @abstractmethod
    def verify_login(self, req: LoginRequest) -> bool:
        pass

    @abstractmethod
    def get_single_user(self, name: str) -> User:
        pass

    @abstractmethod
    def get_multiple_users(self, req: UserSearchRequest) -> list[User]:
        pass

    @abstractmethod
    def register_user(self, usr: User) -> User:
        pass

    @abstractmethod
    def delete_user_by_name(self, name: str) -> None:
        pass

    @abstractmethod
    def update_user(self, req: UserUpdateRequest) -> User:
        pass
