from os import environ
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Bundle, Environment
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object('app.config')

# setup js and scss assets
js = Bundle('main.js', output='output/main.js', filters='jsmin')
css = Bundle('main.scss', output='output/main.css', filters='pyscss')
assets = Environment(app)
assets.register('main_js', js)
assets.register('main_css', css)
app.config['ASSETS_DEBUG'] = "DEBUG" in environ

# setup database
db = SQLAlchemy(app)

from app.models import Category
from app.models import Item

# setup error handlers
from app.errors import errors

app.register_blueprint(errors)

# setup views
from app.views.auth import auth_app
from app.views.category import category_app
from app.views.item import item_app

app.register_blueprint(auth_app)
app.register_blueprint(category_app)
app.register_blueprint(item_app)

# setup api
from app.api.category import category_api_app
from app.api.item import item_api_app
from app.api.auth import auth_api_app

app.register_blueprint(category_api_app)
app.register_blueprint(item_api_app)
app.register_blueprint(auth_api_app)


@app.errorhandler(404)
def page_not_found(e):
    response = {
        'success': False,
        'message': 'Route not found!'
    }

    return jsonify(response), 404


@app.errorhandler(405)
def page_not_found(e):
    response = {
        'success': False,
        'message': 'Method not allowed'
    }

    return jsonify(response), 405
