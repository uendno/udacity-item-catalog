from flask import jsonify


def send_success(data):
    """
    Send success response
    :param data: data to be sent
    :return:
    """
    return jsonify({
        'success': True,
        'data': data
    }), 200


def send_error(message, status_code):
    """
    Send error response
    :param message: message to be sent
    :param status_code: response's status code
    :return:
    """
    return jsonify({
        'success': False,
        'message': message
    }), status_code
