from injector import inject

from ..persistence.base_daos import TicketDao

class TicketService():

    @inject
    def __init__(self, dao: TicketDao) -> None:
        self._dao = dao