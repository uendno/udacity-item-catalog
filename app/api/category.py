from flask import Blueprint, jsonify
from app import db
from app.models import Category, Item
from app.errors import ValidationError

category_api_app = Blueprint('category_api_app', __name__)


@category_api_app.route('/api/categories')
def all_categories():
    categories = db.session.query(Category)

    response = {
        'success': True,
        'data': []
    }

    for category in categories:
        response['data'].append({
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
        })

    return jsonify(response), 200


@category_api_app.route('/api/categories/<string:category_slug>')
def get_category_details(category_slug):
    results = db.session.query(Category).filter_by(slug=category_slug).all()

    if len(results) == 0:
        raise ValidationError('Category not found!')

    category = results[0]

    items = db.session.query(Item).filter_by(category_id=category.id).all()

    response = {
        'success': True,
        'data': {
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'items': []
        }
    }

    for item in items:
        response['data']['items'].append({
            'id': item.id,
            'name': item.name,
            'slug': item.slug,
            'category': {
                'name': item.category.name,
                'id': item.category.id,
                'slug': item.category.slug
            }
        })

    return jsonify(response), 200
