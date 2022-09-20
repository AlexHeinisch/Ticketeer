from injector import inject

from ..repository.ticket_repository import TicketRepository

class TicketService():

    @inject
    def __init__(self, dao: TicketRepository) -> None:
        self._dao = dao
