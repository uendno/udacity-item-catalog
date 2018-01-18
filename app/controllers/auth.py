import json

import jwt
import requests
from flask import Blueprint, request
from oauth2client.client import flow_from_clientsecrets

from app import db, config
from app.models import UserModel, OpenAuthenticationModel
from app.models.errors import ValidationError
from app.helpers.response import send_success, send_error

auth_controller = Blueprint('auth_controller', __name__)

CLIENT_SECRET_FILE = 'app/client_secret.json'
CLIENT_ID = json.loads(open(CLIENT_SECRET_FILE, 'r').read())['web']['client_id']


@auth_controller.route('/auth', methods=['POST'])
def login():
    """
    Exchange Google's authorization code for an access token
    :return:
    """

    # Only accept Google authorization at this time
    if request.args.get('provider') != 'google':
        return send_error('Invalid provider', status_code=400)

    code = request.get_json()['code']
    access_token_data = {}

    if code is None:
        raise ValidationError('Authorization code is missing.')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except Exception as e:

        raise ValidationError('Can\'t use authorization code to exchange for access token')

    gplus_id = credentials.id_token['sub']
    access_token_data['gplus_id'] = gplus_id

    # Get user info
    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    response = requests.get(user_info_url, params=params)
    data = json.loads(response.text)

    oauth = OpenAuthenticationModel.find(data['id'], 'google')

    if oauth is not None:
        user = UserModel.find(user_id=oauth.user_id)

        access_token_data['id'] = user.id
        access_token_data['type'] = oauth.type

    else:

        # Create user and provider_info
        new_user = UserModel(username=data['email'])
        db.session.add(new_user)
        db.session.commit()

        new_oauth = OpenAuthenticationModel(id=data['id'], user_id=new_user.id, type='google')
        db.session.add(new_oauth)
        db.session.commit()

        access_token_data['id'] = new_user.id
        access_token_data['type'] = new_oauth.type

    access_token = jwt.encode(access_token_data, config.JWT_SECRET_KEY, algorithm='HS256')

    return send_success(access_token.decode('utf-8'))
