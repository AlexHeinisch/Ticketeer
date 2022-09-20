import logging
from flask import Blueprint, jsonify, request

# DI
from injector import inject
from ..service.user_service import UserService

# Validation
from ..dto.schemas import UserSchema, UserSearchRequestSchema, UserUpdateRequestSchema
from ..dto.models import User, UserSearchRequest, UserUpdateRequest

# Auth
from ..security.authorization import jwt_required

user = Blueprint('user', __name__)
logger = logging.getLogger(__name__)


@inject
@user.route('/<name>', methods=['GET'])
@jwt_required()
def get_user_by_name(service: UserService, name: str):
    logger.info(f'[GET] single user: name={name}')
    return UserSchema().dump(service.get_single_user(name))

@inject
@user.route('', methods=['GET'])
@jwt_required()
def get_users_by_search(service: UserService):
    req: UserSearchRequest = UserSearchRequestSchema().load(request.args) # type: ignore
    logger.info(f'[GET] users: search-req={req}')
    return jsonify(UserSchema(many=True).dump(service.get_multiple_users(req)))

@inject
@user.route('', methods=['POST'])
def post_user(service: UserService):
    usr: User = UserSchema().load(request.get_json()) # type: ignore
    return UserSchema().dump(service.register_user(usr)), 201

@inject
@user.route('/<name>', methods=['DELETE'])
@jwt_required()
def delete_user(service: UserService, name: str):
    service.delete_user_by_name(name)
    return '', 204

@inject
@user.route('/<name>', methods=['PATCH'])
@jwt_required()
def patch_user(service: UserService, name: str):
    req : UserUpdateRequest = UserUpdateRequestSchema().load(request.get_json()) # type: ignore
    req.username = name
    return UserSchema().dump(service.update_user(req))
