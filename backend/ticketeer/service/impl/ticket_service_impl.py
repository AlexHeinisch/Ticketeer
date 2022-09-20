from injector import inject

from ..ticket_service import TicketService
from ...repository.ticket_repository import TicketRepository

class TicketServiceImpl(TicketService):

    @inject
    def __init__(self, repository: TicketRepository) -> None:
        self._repository = repository
