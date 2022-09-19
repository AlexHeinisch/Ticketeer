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
    ADMIN = 2

### AUTH ###

@dataclass
class LoginRequest():
    username: str
    password: str

### TAGS ###

@dataclass
class Tag():
    id: int
    name: str
    font_color: Optional[str]
    bg_color: Optional[str]


### USER ###

@dataclass
class User():
    username: str
    password: str
    email: str
    icon_id: int = -1
    role: UserRole = UserRole.USER

    def to_sql_format(self):
        return f"('{self.username}', '{self.password}', '{self.email}', {self.icon_id}, '{self.role.name}')"

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'icon_id': self.icon_id,
            'role': self.role.name
        }
    
    def copy(self):
        return User(
            self.username,
            self.password,
            self.email,
            self.icon_id,
            self.role
        )

    def __post_init__(self):
        if self.role and type(self.role) is str:
            self.role = UserRole[self.role.upper()]

@dataclass
class UserSearchRequest():
    username: str
    email: str
    role: UserRole
    num: int = 100
    offset: int = 0

@dataclass
class UserUpdateRequest():
    username: str
    email: str
    old_password: str
    new_password: str
    icon_id: id
    role: UserRole

### TICKET ###

@dataclass
class Ticket():
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
        return User(
            self.username,
            self.password,
            self.email,
            self.icon_id,
            self.role
        )

    def __post_init__(self):
        if self.status and type(self.status) is str:
            self.status = Status[self.status.upper()]

@dataclass
class TicketSearchRequest():
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
class TicketUpdateRequest():
    name: str
    description: str
    assigned_to: str
    created_by: str
    tags: list[int]
    status: Status