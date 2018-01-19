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


def after_scenario(context, scenario):
    # Remove all items

    response = context.client.get('/items')
    json = get_json(response)

    ids = [item['id'] for item in json['data']]

    responses = remove_items(ids, client=context.client)

    for response in responses:
        assert response.status_code == 200
