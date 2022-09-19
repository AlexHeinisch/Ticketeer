from flask import Blueprint

# Errors
from marshmallow import ValidationError
from .custom_errors import ConflictError, NotFoundError, AuthorizationError, PermissionError

error_handlers = Blueprint('error_handlers', __name__)

@error_handlers.app_errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    return e.messages, 422, {'Content-type': 'application/json'}

@error_handlers.app_errorhandler(ConflictError)
def handle_conflict_error(e: ConflictError):
    return e.messages, 409, {'Content-type': 'application/json'}

@error_handlers.app_errorhandler(NotFoundError)
def handle_notfound_error(e: NotFoundError):
    return e.messages, 404, {'Content-type': 'application/json'}

@error_handlers.app_errorhandler(AuthorizationError)
def handle_authorization_error(e: AuthorizationError):
    return e.messages, 401, {'Content-type': 'application/json'}

@error_handlers.app_errorhandler(PermissionError)
def handle_permission_error(e: PermissionError):
    return e.messages, 403, {'Content-type': 'application/json'}
