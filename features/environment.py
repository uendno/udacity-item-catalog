import os

from app import app
from manage import init_db, seed_categories
from features.steps.utils import get_json, remove_items

DB_URI = 'sqlite:///test.db'


def before_feature(context, feature):
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.testing = True
    context.client = app.test_client()
    with app.app_context():
        init_db()
        seed_categories()


def after_feature(context, feature):
    os.unlink('app/test.db')

