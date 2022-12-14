from flask import Blueprint, jsonify, request, current_app
import datetime
import jwt
import werkzeug.exceptions
from typing import cast

from injector import inject

from ticketeer.error.custom_errors import AuthorizationError

from ticketeer.service.user_service import UserService

from ticketeer.dto.schemas import LoginRequestSchema
from ticketeer.dto.dtos import LoginRequestDto, UserRole

authentication = Blueprint('authentication', __name__)

@inject
@authentication.route('/login', methods=['GET', 'POST'])
def login(service: UserService):
    body = request.get_json()
    if not body:
        raise werkzeug.exceptions.BadRequest()
    obj: LoginRequestDto = cast(LoginRequestDto, LoginRequestSchema().load(body))
    try:
        user = service.get_user_by_name(obj.username)
        if user and service.verify_login(obj):
            token = generate_token(user.id, user.username, user.role, current_app.config['SECRET_KEY'])
            return {'token' : token}
    except:
        ...
    raise AuthorizationError('could not authenticate')

def generate_token(id: int, username: str, role: UserRole, secret: str):
    return jwt.encode(
            {
                'id': id,
                'username' : username,
                'role': role.name,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=14)
            }, 
            secret, 
            "HS256")
