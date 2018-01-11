from flask import Blueprint, jsonify
import traceback


class ItemCatalogError(Exception):
    status_code = 500


class ValidationError(ItemCatalogError):
    status_code = 400


class UnauthorizedError(ItemCatalogError):
    status_code = 401


errors = Blueprint('errors', __name__)


@errors.app_errorhandler(ItemCatalogError)
def handle_error(error):
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


@errors.app_errorhandler(Exception)
def handler_unexpected_error(error):
    print(error)
    traceback.print_tb(error.__traceback__)

    status_code = 500
    success = False
    response = {
        'success': success,
        'message': 'An unexpected error has occurred'
    }

    return jsonify(response), status_code


