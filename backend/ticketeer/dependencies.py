from ticketeer.service.ticket_service import TicketService
from ticketeer.service.impl.ticket_service_impl import TicketServiceImpl
from ticketeer.service.user_service import UserService
from ticketeer.service.impl.user_service_impl import UserServiceImpl

from ticketeer.repository.user_repository import UserRepository
from ticketeer.repository.impl.sqlalchemy_user_repository import SQLAlchemyUserRepository

from flask_sqlalchemy import SQLAlchemy

from ticketeer import db
from injector import Binder, singleton

def configure(binder: Binder):
    binder.bind(SQLAlchemy, to=db, scope=singleton)

    binder.bind(TicketService, to=TicketServiceImpl, scope=singleton)
    binder.bind(UserService, to=UserServiceImpl, scope=singleton)

    binder.bind(UserRepository, to=SQLAlchemyUserRepository, scope=singleton)
