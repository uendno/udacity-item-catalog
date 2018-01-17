from functools import wraps

import jwt
from flask import request

from app import config
from app.models.errors import UnauthorizedError


def auth_enabled(is_required):
    """
    Check access token if it's required and then decode it
    :param is_required:
    :return:
    """
    def decorated(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            access_token = request.headers.get('Authorization')

            if is_required:
                if access_token is None:
                    raise UnauthorizedError('Access token is required')

            if access_token is not None:
                try:
                    decoded = jwt.decode(access_token, config.JWT_SECRET_KEY, algorithms=['HS256'])
                    kwargs['user_info'] = decoded
                except Exception:
                    raise UnauthorizedError

            return f(*args, **kwargs)

        return wrapper

    return decorated
