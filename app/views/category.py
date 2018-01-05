from flask import Blueprint, render_template, session as login_session, make_response
import json
from app import db
from app.models import Category, Item

category_app = Blueprint('category_app', __name__,
                         template_folder='templates')


@category_app.route('/')
def index():
    categories = db.session.query(Category)
    logged_in = login_session.get('access_token') is not None
    items = db.session.query(Item).order_by(Item.created_date.desc()).limit(10).all()

    return render_template('index.html', categories=categories, logged_in=logged_in, items=items)


@category_app.route('/catalog/<string:catagory_slug>/items')
def category(catagory_slug):
    logged_in = login_session.get('access_token') is not None
    categories = db.session.query(Category)
    category = db.session.query(Category).filter_by(slug=catagory_slug).one()
    items = db.session.query(Item).filter_by(category_id=category.id).all()

    return render_template('category.html', categories=categories, items=items, logged_in=logged_in, category=category)


@category_app.route('/catalog.json')
def catalog_json():
    categories = db.session.query(Category)

    result = {
        'Category': []
    }

    for category in categories:
        items = db.session.query(Item).filter_by(category_id=category.id).all()
        items_data = []

        for item in items:
            items_data.append({'cat_id': item.category_id, 'description': item.description, 'id': item.id,
                               'title': item.name})

        category_data = {'id': category.id, 'name': category.name, 'Item': items_data}
        result['Category'].append(category_data)

    print(result)

    response = make_response(json.dumps(result, indent=4, sort_keys=True), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
