from .service.ticket_service import TicketService
from .service.user_service import UserService

from .repository.user_repository import UserRepository
from .repository.impl.sqlalchemy_user_repository import SQLAlchemyUserRepository

from flask_sqlalchemy import SQLAlchemy

from .extensions import db
from injector import Binder, singleton

def configure(binder: Binder):
    binder.bind(SQLAlchemy, to=db, scope=singleton)

    binder.bind(TicketService, to=TicketService, scope=singleton)
    binder.bind(UserService, to=UserService, scope=singleton)

    binder.bind(UserRepository, to=SQLAlchemyUserRepository, scope=singleton)
