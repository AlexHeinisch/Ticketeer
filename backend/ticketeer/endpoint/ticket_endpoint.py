from flask import Blueprint

from injector import inject

from ..service.ticket_service import TicketService
from ..security.authorization import jwt_required


ticket = Blueprint('ticket', __name__)

@inject
@ticket.route('/<id>', methods=['GET'])
@jwt_required()
def get_ticket_by_id(service: TicketService, id: int):
    return 'Hellö'

@inject
@ticket.route('/', methods=['GET'])
@jwt_required()
def get_tickets_by_search(service: TicketService):
    return 'Hellö'

@inject
@ticket.route('/', methods=['POST'])
@jwt_required()
def post_ticket(service: TicketService):
    return 'Hellö'

@inject
@ticket.route('/', methods=['DELETE'])
@jwt_required()
def delete_ticket(service: TicketService):
    return 'Hellö'

@inject
@ticket.route('/', methods=['PATCH'])
@jwt_required()
def patch_ticket(service: TicketService):
    return 'Hellö'