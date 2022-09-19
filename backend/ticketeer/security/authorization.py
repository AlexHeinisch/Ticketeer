from functools import wraps
from flask import request, g, current_app
from jwt import DecodeError, decode
from ..error.custom_errors import AuthorizationError, PermissionError
from ..models import UserRole


def jwt_required(allowed_roles = []):
    if allowed_roles:
        allowed_roles = [r.name for r in allowed_roles]

    def decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            obj = request.headers.get("authorization", None)
            if not obj:
                raise AuthorizationError('no authorization token provided')

            try:
                token = obj.split(' ')[1]
                resp = decode(token, current_app.config['SECRET_KEY'], verify=True, algorithms=['HS256'])

                # check advanced permissions specified in the decorator
                if allowed_roles and (resp['role'] not in allowed_roles):
                    raise PermissionError('forbidden')
                
                g.user = resp['username']
                g.role = UserRole[resp['role']]
            except DecodeError:
                raise AuthorizationError('invalid authorization token provided')

            return f(*args, **kwargs)

        return wrap
    return decorator