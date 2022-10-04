from sqlalchemy import Enum, false
from ticketeer import db
from ticketeer.dto.dtos import UserDto, UserRole

class Tag(db.Model): # type: ignore  [pyright thinking Model is wrong here]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  

class User(db.Model): # type: ignore
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(100))
    password_hash = db.Column('password_hash', db.String(255))
    email = db.Column('email', db.String(255))
    role = db.Column('role', Enum(UserRole))

    def __init__(self, username, password_hash, email, id=-1, role=UserRole.USER) -> None:
        super().__init__()
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role

    def __eq__(self, __o: object) -> bool:
        if type(__o) is not User:
            return False
        return __o.id == self.id and __o.username == self.username and __o.password_hash == self.password_hash and __o.email == self.email and __o.role == self.role

    def to_dto(self) -> UserDto:
        return UserDto(
            id=self.id,
            username=self.username,
            password='',
            email = self.email,
            role = self.role
        )

