from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

### ENUMS

class Status(str, Enum):
    OPEN = 1
    INPROGRESS = 2
    DONE = 3
    UNKNOWN = 4

class UserRole(str, Enum):
    USER = 1
    MODERATOR = 2
    ADMIN = 3

### AUTH ###

@dataclass
class LoginRequestDto():
    username: str
    password: str
    

### TAGS ###

@dataclass
class TagDto():
    id: int
    name: str
    font_color: Optional[str]
    bg_color: Optional[str]


### USER ###

@dataclass
class UserDto():
    id: int
    username: str
    password_hash: str
    email: str
    icon_id: int = -1
    role: UserRole = UserRole.USER

    def to_sql_format(self):
        return f"({id}, '{self.username}', '{self.password_hash}', '{self.email}', {self.icon_id}, '{self.role.name}')"

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password_hash,
            'email': self.email,
            'icon_id': self.icon_id,
            'role': self.role.name
        }
    
    def copy(self):
        return UserDto(
            self.id,
            self.username,
            self.password_hash,
            self.email,
            self.icon_id,
            self.role
        )

    def __post_init__(self):
        if self.role and type(self.role) is str:
            self.role = UserRole[self.role.upper()]

@dataclass
class UserRegisterRequestDto():
    username: str
    password: str
    email: str

@dataclass
class UserSearchRequestDto():
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None
    num: int = 100
    offset: int = 0

@dataclass
class UserUpdateRequestDto():
    id: int = -1
    username: Optional[str] = None
    email: Optional[str] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None
    icon_id: Optional[int] = None
    role: Optional[UserRole] = None

### TICKET ###

@dataclass
class TicketDto():
    id: int
    name: str
    description: str
    assigned_to: str
    assigned_to_changed_date: datetime
    created_by: str
    creation_date: datetime
    image_ids: list[int]
    tags: list[int]
    status: Status

    def to_sql_format_base(self):
        return f"('{self.name}', '{self.description}', '{self.assigned_to}', '{self.assigned_to_changed_date}', \
            '{self.created_by}', '{self.creation_date}', '{self.status}')"

    def to_sql_format_image_ids(self):
        return [f'({self.id}, {x})' for x in self.image_ids]
    
    def to_sql_format_tags(self):
        return [f'({self.id}, {x})' for x in self.tags]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'assigned_to': self.assigned_to,
            'assigned_to_changed_date': self.assigned_to_changed_date,
            'created_by': self.created_by,
            'creation_date': self.creation_date,
            'image_ids': self.image_ids,
            'tags': self.tags,
            'status': self.status
        }
    
    def copy(self):
        return TicketDto(
            self.id,
            self.name,
            self.description,
            self.assigned_to,
            self.assigned_to_changed_date,
            self.created_by,
            self.creation_date,
            self.image_ids,
            self.tags,
            self.status
        )

    def __post_init__(self):
        if self.status and type(self.status) is str:
            self.status = Status[self.status.upper()]

@dataclass
class TicketSearchRequestDto():
    name: str
    description: str
    assigned_to: str
    assigned_changed_date_before: datetime
    assigned_changed_date_after: datetime
    created_by: str
    creation_date_before: datetime
    creation_date_before_after: datetime
    tags: list[int]
    status: Status
    num: int = 100
    offset: int = 0

@dataclass
class TicketUpdateRequestDto():
    name: str
    description: str
    assigned_to: str
    created_by: str
    tags: list[int]
    status: Status
