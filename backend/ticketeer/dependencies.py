from .service.ticket_service import TicketService
from .service.impl.ticket_service_impl import TicketServiceImpl
from .service.user_service import UserService
from .service.impl.user_service_impl import UserServiceImpl

from .repository.user_repository import UserRepository
from .repository.impl.sqlalchemy_user_repository import SQLAlchemyUserRepository

from flask_sqlalchemy import SQLAlchemy

from .import db
from injector import Binder, singleton

def configure(binder: Binder):
    binder.bind(SQLAlchemy, to=db, scope=singleton)

    binder.bind(TicketService, to=TicketServiceImpl, scope=singleton)
    binder.bind(UserService, to=UserServiceImpl, scope=singleton)

    binder.bind(UserRepository, to=SQLAlchemyUserRepository, scope=singleton)
