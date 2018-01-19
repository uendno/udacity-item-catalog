from flask import Blueprint

from app.models.errors import ItemCatalogError
from app.helpers.response import send_error
from app.extensions import logger

errors_controller = Blueprint('errors_controller', __name__)


@errors_controller.app_errorhandler(ItemCatalogError)
def handle_error(error):
    """
    Handle ItemCatalogError errors
    :param error:
    :return:
    """

    logger.warn(error)

    if len(error.args) > 0:
        message = error.args[0]
        errors = error.args[1] if len(error.args) > 1 else None
    else:
        message = ''
        errors = None

    return send_error(message, status_code=error.status_code, errors=errors)


@errors_controller.app_errorhandler(Exception)
def handler_unexpected_error(error):
    """
    Handle general errors
    :param error:
    :return:
    """

    logger.exception(error)

    return send_error('An unexpected error has occurred', status_code=500)
