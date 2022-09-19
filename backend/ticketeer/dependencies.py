from injector import singleton, Binder

# Connector dependencies
from .persistence.connectors.psql_connector import PostgresConnector

# Persistance dependencies
from .persistence.base_daos import TicketDao, UserDao
from .persistence.implementations.dummy_daos import DummyTicketDao, DummyUserDao
from .persistence.implementations.postgres_daos import PostgresTicketDao, PostgresUserDao

# Service dependencies
from .service.ticket_service import TicketService
from .service.user_service import UserService


def configure(binder: Binder) -> None:
    binder.bind(PostgresConnector, to=PostgresConnector, scope=singleton)

    binder.bind(TicketDao, to=PostgresTicketDao, scope=singleton)
    binder.bind(UserDao, to=PostgresUserDao, scope=singleton)

    binder.bind(TicketService, to=TicketService, scope=singleton)
    binder.bind(UserService, to=UserService, scope=singleton)