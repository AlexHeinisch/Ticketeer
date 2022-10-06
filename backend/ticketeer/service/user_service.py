from ticketeer.dto.dtos import UserDto, LoginRequestDto, UserRegisterRequestDto, UserSearchRequestDto, UserUpdateRequestDto
from abc import ABC, abstractmethod

from ticketeer.security.authorization import CurrentPermissions

class UserService(ABC):

    @abstractmethod
    def verify_login(self, req: LoginRequestDto) -> bool:
        ...

    @abstractmethod
    def get_user_by_id(self, id: int) -> UserDto:
        ...

    @abstractmethod
    def get_user_by_name(self, name: str) -> UserDto:
        ...

    @abstractmethod
    def get_multiple_users(self, req: UserSearchRequestDto) -> list[UserDto]:
        ...

    @abstractmethod
    def register_user(self, usr_dto: UserRegisterRequestDto) -> UserDto:
        ...

    @abstractmethod
    def delete_user_by_name(self, name: str) -> None:
        ...

    @abstractmethod
    def delete_user_by_id(self, id: int) -> None:
        ...

    @abstractmethod
    def update_user(self, req: UserUpdateRequestDto, perm: CurrentPermissions) -> UserDto:
        ...
