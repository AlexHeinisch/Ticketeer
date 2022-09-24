from ticketeer.dto.dtos import UserDto, LoginRequestDto, UserSearchRequestDto, UserUpdateRequestDto
from abc import ABC, abstractmethod

class UserService(ABC):

    @abstractmethod
    def verify_login(self, req: LoginRequestDto) -> bool:
        pass

    @abstractmethod
    def get_user_by_name(self, name: str) -> UserDto:
        pass

    @abstractmethod
    def get_multiple_users(self, req: UserSearchRequestDto) -> list[UserDto]:
        pass

    @abstractmethod
    def register_user(self, usr_dto: UserDto) -> UserDto:
        pass

    @abstractmethod
    def delete_user_by_name(self, name: str) -> None:
        pass

    @abstractmethod
    def update_user(self, req: UserUpdateRequestDto) -> UserDto:
        pass
