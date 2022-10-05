from abc import ABC, abstractmethod
from ticketeer.dto.dtos import UserDto, UserRegisterRequestDto, UserSearchRequestDto, UserUpdateRequestDto

class UserRepository(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_user_by_name(self, name: str) -> UserDto | None:
        ...

    @abstractmethod
    def get_user_by_id(self, id: int) -> UserDto | None:
        ...

    @abstractmethod
    def delete_user_by_name(self, name: str) -> None:
        ...

    @abstractmethod
    def delete_user_by_id(self, id: int) -> None:
        ...

    @abstractmethod
    def insert_user(self, usr_dto: UserRegisterRequestDto) -> UserDto:
        ...

    @abstractmethod
    def get_users_by_search_req(self, req: UserSearchRequestDto) -> list[UserDto]:
        ...

    @abstractmethod
    def update_user(self, req: UserUpdateRequestDto) -> UserDto:
        ...
