import logging
from werkzeug.exceptions import BadRequest
from typing import cast
from flask import Blueprint, jsonify, request

# DI
from injector import inject
from ticketeer.service.user_service import UserService

# Validation
from ticketeer.dto.schemas import UserRegisterRequestSchema, UserSchema, UserSearchRequestSchema, UserUpdateRequestSchema
from ticketeer.dto.dtos import UserRegisterRequestDto, UserUpdateRequestDto, UserSearchRequestDto, UserSearchRequestDto

# Auth
from ..security.authorization import jwt_required

user = Blueprint('user', __name__)
logger = logging.getLogger(__name__)


@inject
@user.route('/<id>', methods=['GET'])
#@jwt_required()
def get_user_by_id(service: UserService, id: int):
    logger.info(f'[GET] single user: id={id}')
    return UserSchema().dump(service.get_user_by_id(id))

@inject
@user.route('', methods=['GET'])
#@jwt_required()
def get_users_by_search(service: UserService):
    req: UserSearchRequestDto = cast(UserSearchRequestDto, UserSearchRequestSchema().load(request.args))
    logger.info(f'[GET] users: search-req={req}')
    return jsonify(UserSchema(many=True).dump(service.get_multiple_users(req)))

@inject
@user.route('', methods=['POST'])
def post_user(service: UserService):
    body = request.get_json()
    if not body:
        raise BadRequest()
    req: UserRegisterRequestDto = cast(UserRegisterRequestDto, UserRegisterRequestSchema().load(body))
    return UserSchema().dump(service.register_user(req)), 201

@inject
@user.route('/<id>', methods=['DELETE'])
#@jwt_required()
def delete_user(service: UserService, id: int):
    service.delete_user_by_id(id)
    return '', 204

@inject
@user.route('/<name>', methods=['PATCH'])
#@jwt_required()
def patch_user(service: UserService, name: str):
    body = request.get_json()
    if not body:
        raise BadRequest()
    req : UserUpdateRequestDto = cast(UserUpdateRequestDto, UserUpdateRequestSchema().load(body))
    req.username = name
    return UserSchema().dump(service.update_user(req))
