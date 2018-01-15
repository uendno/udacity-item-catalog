from flask import Blueprint, jsonify
import traceback
from app.models.errors import ItemCatalogError

errors_controller = Blueprint('errors_controller', __name__)


@errors_controller.app_errorhandler(ItemCatalogError)
def handle_error(error):
    """
    Handle ItemCatalogError errors
    :param error:
    :return:
    """

    traceback.print_tb(error.__traceback__)

    if len(error.args) > 0:
        message = error.args[0]
    else:
        message = ''

    status_code = error.status_code
    success = False
    response = {
        'success': success,
        'message': message
    }

    return jsonify(response), status_code


@errors_controller.app_errorhandler(Exception)
def handler_unexpected_error(error):
    """
    Handle general errors
    :param error:
    :return:
    """

    print(error)
    traceback.print_tb(error.__traceback__)

    status_code = 500
    success = False
    response = {
        'success': success,
        'message': 'An unexpected error has occurred'
    }

    return jsonify(response), status_code
