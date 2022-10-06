from ctypes import ArgumentError
from datetime import datetime
from functools import update_wrapper, wraps
from inspect import Signature, signature
import inspect
from injector import inject
from jwt import DecodeError, decode
from ticketeer.error.custom_errors import AuthorizationError, PermissionError
from ticketeer.dto.dtos import UserRole
from flask import Flask
from flask.wrappers import Request
import re

class CurrentPermissions():
    user_id: int
    user_name: str
    user_role: UserRole 

    def __init__(self, id: int, user_name: str, user_role: UserRole) -> None:
        self.user_id = id
        self.user_name = user_name
        self.user_role = user_role

    def __repr__(self) -> str:
        return f'<CurrentPermissions(user_id={self.user_id}, user_name="{self.user_name}", user_role={self.user_role})>'


def jwt_required(*permission_options):

    def decorator(f):
        @_wrap_and_inject_wrapper(f)
        def wrapper(__req: Request, __app: Flask, *args, **kwargs):

            # check if function needs manual permission injection
            permission_param_name = None
            for name,parameter in inspect.signature(f).parameters.items():
                if f'{CurrentPermissions.__module__}.{CurrentPermissions.__name__}' in str(parameter):
                    permission_param_name = name
                    break

            # get the 'authorization' header from the request
            auth_header = __req.headers.get("authorization", None)
            if not auth_header:
                raise AuthorizationError('no authorization token provided')

            try:
                # check if the bearer token header is valid
                split_str = auth_header.split(' ')
                if len(split_str) < 2 or 'Bearer' not in split_str[0]:
                    raise AuthorizationError('invalid bearer token format')

                # split the token and decode it to get the individual values
                token = split_str[1]
                resp = decode(token, __app.config['SECRET_KEY'], verify=True, algorithms=['HS256'])

                # check if token is still valid
                if resp['exp'] < datetime.utcnow().timestamp():
                    raise AuthorizationError('token no longer valid')

                # check advanced permissions specified in the decorator
                if len(permission_options) > 0:
                    if not _has_permission(permission_options, resp, kwargs):
                        raise PermissionError('forbidden')
               
                # inject current permissions into endpoint function if required
                if permission_param_name:
                    kwargs[permission_param_name] = CurrentPermissions(id=resp['id'], user_name=resp['username'], user_role=resp['role'])
                return f(*args, **kwargs)
            except DecodeError:
                raise AuthorizationError('invalid authorization token provided')

        return wrapper
    return decorator

def _has_permission(perm_options, token_info, arguments):
    """
    Method used to check custom permission options for a certain endpoint method.
    To give the user customizability the first level of possible permission conditions is OR-linked.

    This means that a perm_options list of [Something1, Something2, Something3] is evaluated like Something1 OR Something2 OR Something3.
    To give the user access to AND-linking as-well a sub-list can be provided one level deeper which is then AND-linked.

    An example for both OR-and-AND-linked conditions:

    perm_options=[[Something1, Something2], Something3]
    This is evaluated as (Something1 AND Something2) OR Something3

    These Somethings can either be simple UserRole indicating that the calling user needs to have a ceratin role or
    it can be a string rule that checks if a value in the arguments passed or the jwt token matches a certain value.

    For string rules placeholders can be used in which the respective values are automatically imported. These include:
    - <param> Request parameter
    - BEARER[id] Field in the bearer/jwt token
    """

    # if simply a role was passed it is assumed that the current user is required to have that role
    def check_role(param: UserRole):
        return token_info['role'] == param.name
            
    def check_string_rule(param: str):
        # replace request parameter placeholders with actual values
        for r in re.findall('<.*?>', param):
            param = param.replace(r, str(arguments[r[1:-1]]))
        # replace jwt token placeholders with actual values
        for r in re.findall('BEARER\\[.*?\\]', param):
            param = param.replace(r, str(token_info[r[7:-1]]))
       
        # split rule in its 3 parts
        split_str = param.split(' ')
        if len(split_str) != 3:
            raise ArgumentError

        # try converting arg1 and arg2 to numeric
        arg1, arg2 = None, None
        try:
            arg1 = float(split_str[0])
            arg2 = float(split_str[2])
        except:
            arg1, arg2 = split_str[0], split_str[2]

        # compare arg1 and arg2 depending on the operator specified
        match(split_str[1]):
            case '==':
                return arg1 == arg2
            case '<':
                return type(arg1) is float and type(arg2) is float and arg1 < arg2
            case '>':
                return type(arg1) is float and type(arg2) is float and arg1 > arg2
            case '!=':
                return arg1 == arg2
        raise ArgumentError

    allowed = False
    for rule in perm_options:
        if type(rule) is UserRole:
            allowed = allowed or check_role(rule) 
        elif type(rule) is str:
            allowed = allowed or check_string_rule(rule)
        elif type(rule) is list:
            tmp_allowed = True
            for sub_rule in rule:
                if type(sub_rule) is UserRole:
                    if not check_role(sub_rule):
                        tmp_allowed = False
                        break
                elif type(sub_rule) is str:
                    if not check_string_rule(sub_rule):
                        tmp_allowed = False
                        break
                else:
                    print('Unknown rule!')
                    tmp_allowed = False
            allowed = allowed or tmp_allowed
        else:
            print('Unknown rule!')

    return allowed

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
        for _,v in signature(f).parameters.items():
            if not (str(v) == '*args' or str(v) == '**kwargs'):
                params.append(v)
        for _, v in sig.parameters.items():
            params.append(v)
        wrapper.__signature__ = Signature(parameters=params, return_annotation=sig.return_annotation)
        update_wrapper(wrapper, wraps_function)
        return wrapper
    return decorator




