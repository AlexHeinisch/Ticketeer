from flask import Blueprint, jsonify, request, current_app
import datetime
import jwt

from injector import inject

from ticketeer.error.custom_errors import AuthorizationError

from ticketeer.service.user_service import UserService

from ticketeer.dto.schemas import LoginRequestSchema
from ticketeer.dto.dtos import LoginRequestDto

authentication = Blueprint('authentication', __name__)

@inject
@authentication.route('/login', methods=['GET', 'POST'])
def login(service: UserService):
    obj: LoginRequestDto = LoginRequestSchema().load(request.get_json()) # type: ignore
    user = service.get_user_by_id(obj.username)
    if user and service.verify_login(obj):
        token = generate_token(user.username, user.role, current_app.config['SECRET'])
        return {'token' : token}
    raise AuthorizationError('could not authenticate')

def generate_token(username, role, secret):
    token = jwt.encode(
            {
                'username' : username,
                'role': role.name,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
            }, 
            secret, 
            "HS256")
    return token
