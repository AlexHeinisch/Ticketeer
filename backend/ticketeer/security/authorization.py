from datetime import datetime
from functools import update_wrapper, wraps
from inspect import Signature, signature
from injector import inject
from jwt import DecodeError, decode
from ticketeer.error.custom_errors import AuthorizationError, PermissionError
from ticketeer.dto.dtos import CurrentPermissions, UserRole
from flask import Flask
from flask.wrappers import Request

def jwt_required(allowed_roles = []):
    if allowed_roles:
        allowed_roles = [r.name for r in allowed_roles]

    def decorator(f):
        @_wrap_and_inject_wrapper(f)
        def wrapper(req: Request, app: Flask, *args, **kwargs):
            obj = req.headers.get("authorization", None)
            if not obj:
                raise AuthorizationError('no authorization token provided')

            try:
                token = obj.split(' ')[1]
                resp = decode(token, app.config['SECRET_KEY'], verify=True, algorithms=['HS256'])

                if resp['exp'] < datetime.utcnow():
                    raise AuthorizationError('token no longer valid')

                # check advanced permissions specified in the decorator
                if allowed_roles and (resp['role'] not in allowed_roles):
                    raise PermissionError('forbidden')
               
                f.__current_permissions__ = CurrentPermissions(id=resp['id'], user_name=resp['username'], user_role=resp['role'])
                return f(*args, **kwargs)
            except DecodeError:
                raise AuthorizationError('invalid authorization token provided')


        return wrapper
    return decorator

def _wrap_and_inject_wrapper(wraps_function):
    def decorator(f):
        @inject
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        # signature manipulation used to make the decorator this helper
        # is used on use injection while hiding the injected parameters
        # from the actual function that is decorated
        sig = signature(wraps_function)
        params = []
        for n,v in signature(f).parameters.items():
            if not (str(v) == '*args' or str(v) == '**kwargs'):
                params.append(v)
        for n, v in sig.parameters.items():
            params.append(v)
        wrapper.__signature__ = Signature(parameters=params, return_annotation=sig.return_annotation)
        update_wrapper(wrapper, wraps_function)
        return wrapper
    return decorator




