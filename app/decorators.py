from flask import request
import jwt
from app import config
from app.models.errors import UnauthorizedError
from functools import wraps


def auth_enabled(is_required):
    def decorated(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            access_token = request.headers.get('Authorization')

            if is_required:
                if access_token is None:
                    raise UnauthorizedError('Access token is required')

            if access_token is not None:
                try:
                    decoded = jwt.decode(access_token, config.SECRET_KEY, algorithms=['HS256'])
                    kwargs['decoded'] = decoded
                except Exception:
                    raise UnauthorizedError

            return f(*args, **kwargs)

        return wrapper

    return decorated
