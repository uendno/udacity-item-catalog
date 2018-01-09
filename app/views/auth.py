from flask import Blueprint, render_template, session as login_session, request, make_response, redirect
import random, string
import requests
import random
import string
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
from app import db
from app.models import User, GoogleProvider

auth_app = Blueprint('auth_app', __name__,
                     template_folder='templates')

CLIENT_SECRET_FILE = 'app/client_secret.json'
CLIENT_ID = json.loads(open(CLIENT_SECRET_FILE, 'r').read())['web']['client_id']


# show login page
@auth_app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# login with google
@auth_app.route('/gconnect', methods=['POST'])
def g_connect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope='')
        oauth_flow.redirect_uri = 'http://localhost:5000'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    # Check that the access token is valid
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']

    # Verify that the access token is used for the intended user.
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps('Token\'s client ID does not match app\'s'), 401)
        print('Token \'s client ID doese not match app\'s.')
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

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

        login_session['username'] = user.username
        login_session['id'] = user.id
        login_session['type'] = user.providerType
    else:

        # create user and provider_info
        new_provider_info = GoogleProvider(id=data['id'], email=data['email'], access_token=credentials.access_token,
                                           name=data['name'], picture=data['picture'])
        new_user = User(username=data['email'], providerType='google', providerId=data['id'])
        db.session.add(new_provider_info)
        db.session.add(new_user)
        db.session.commit()

        login_session['username'] = new_user.username
        login_session['id'] = new_user.id
        login_session['type'] = new_user.providerType

    response = make_response(json.dumps('OK'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


# logout (disconnect from google if needed)
@auth_app.route('/gdisconnect')
def g_disconnect():
    # Only disconnect a connected user
    print(login_session)
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP GET request to revoke current token.
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    # Reset the user's session
    try:
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['id']
        del login_session['type']
    except KeyError:
        pass

    response = make_response(json.dumps('Successfully disconnected'), 200)
    response.headers['Content-Type'] = 'application/json'
    return redirect('/')
