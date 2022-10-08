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

    def __repr__(self) -> str:
        return f'User(id={self.id}, username="{self.username}", email="{self.email}", password_hash="{self.password_hash}", role={self.role})'

    @staticmethod
    def to_dto(usr) -> UserDto:
        return UserDto(
            id=usr.id,
            username=usr.username,
            password_hash=usr.password_hash,
            email = usr.email,
            role = usr.role
        )

    @staticmethod
    def create_copy(usr):
        return User(
            id=usr.id,
            username=usr.username,
            password_hash=usr.password_hash,
            email = usr.email,
            role = usr.role
        )

