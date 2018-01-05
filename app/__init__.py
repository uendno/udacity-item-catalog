from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Bundle, Environment

app = Flask(__name__)
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

# setup views
from app.views.auth import auth_app
from app.views.category import category_app
from app.views.item import item_app

app.register_blueprint(auth_app)
app.register_blueprint(category_app)
app.register_blueprint(item_app)
