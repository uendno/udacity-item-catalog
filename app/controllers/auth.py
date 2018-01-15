from flask import Blueprint, request, jsonify
import requests
from oauth2client.client import flow_from_clientsecrets
import json
from app import db, config
from app.models import User, GoogleProvider
from app.models.errors import ValidationError
import jwt

auth_controller = Blueprint('auth_controller', __name__)

CLIENT_SECRET_FILE = 'app/client_secret.json'
CLIENT_ID = json.loads(open(CLIENT_SECRET_FILE, 'r').read())['web']['client_id']


# login with google
@auth_controller.route('/api/gconnect', methods=['POST'])
def g_connect():
    """
    Exchange Google's authorization code for an access token
    :return:
    """

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

        raise ValidationError('Can\' use authorization code to exchange for access token')

    gplus_id = credentials.id_token['sub']
    access_token_data['gplus_id'] = gplus_id

    # Get user info
    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(user_info_url, params=params)
    data = json.loads(answer.text)

    provider_infos = db.session.query(GoogleProvider).filter_by(id=data['id']).all()

    if len(provider_infos) > 0:
        user = db.session.query(User).filter_by(providerType='google', providerId=provider_infos[0].id).one()
        # update provider info
        provider_infos[0].access_token = credentials.access_token
        db.session.add(provider_infos[0])
        db.session.commit()

        access_token_data['id'] = user.id
        access_token_data['type'] = user.providerType

    else:

        # create user and provider_info
        new_provider_info = GoogleProvider(id=data['id'], email=data['email'], access_token=credentials.access_token,
                                           name=data['name'], picture=data['picture'])
        new_user = User(username=data['email'], providerType='google', providerId=data['id'])
        db.session.add(new_provider_info)
        db.session.add(new_user)
        db.session.commit()

        access_token_data['id'] = new_user.id
        access_token_data['type'] = new_user.providerType

    access_token = jwt.encode(access_token_data, config.SECRET_KEY, algorithm='HS256')

    return jsonify({
        'data': access_token.decode('utf-8'),
        'success': True
    }), 200
