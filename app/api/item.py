from flask import Blueprint, jsonify, request
from app import db
from app.models import Item, Category
from app.errors import ValidationError
from app.decorators import auth_enabled
from jsonschema import validate
from slugify import slugify

item_api_app = Blueprint('item_api_app', __name__)


@item_api_app.route('/api/items/<int:item_id>', methods=['GET'])
def item_details(item_id):
    results = db.session.query(Item).filter_by(id=item_id).all()

    if len(results) == 0:
        raise ValidationError('Item not found!')

    item = results[0]

    response = {
        'success': True,
        'data': {
            'id': item.id,
            'name': item.name,
            'slug': item.slug,
            'category': {
                'name': item.category.name,
                'id': item.category.id,
                'slug': item.category.slug
            },
            'description': item.description,
            'userId': item.user_id
        },
    }

    return jsonify(response), 200


@item_api_app.route('/api/items/latest')
def latest_items():
    items = db.session.query(Item).order_by(Item.created_date.desc()).limit(10).all()

    response = {
        'success': True,
        'data': []
    }

    for item in items:
        response['data'].append({
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


@item_api_app.route('/api/items/<int:item_id>', methods=['PUT'])
@auth_enabled(is_required=True)
def update_item(item_id, decoded):
    data = request.get_json()

    # validate json

    schema = {
        'name': 'string',
        'description': 'string',
        'categoryId': 'number',
        'required': ['name', 'description', 'categoryId']
    }

    try:
        validate(data, schema)
    except Exception as e:
        raise ValidationError(e.args[0])
        pass

    # validate item id

    results = db.session.query(Item).filter_by(id=item_id, user_id=decoded['id']).all()

    if len(results) == 0:
        raise ValidationError('Item not found!')

    item = results[0]

    # validate item name

    valid = Item.validate_slug(slugify(data['name']), item.id)

    if not valid:
        raise ValidationError('An item with the same name has already been added. Please try another name.')

    # validate category id

    category = Category.find_by_id(data['categoryId'])

    if category is None:
        raise ValidationError('Invalid category Id')

    item.name = data['name']
    item.description = data['description']
    item.category_id = data['categoryId']
    item.slug = slugify(item.name)

    db.session.add(item)
    db.session.commit()

    response = {
        'success': True,
        'data': {
            'id': item.id,
            'name': item.name,
            'slug': item.slug,
            'category': {
                'name': item.category.name,
                'id': item.category.id,
                'slug': item.category.slug
            },
            'description': item.description,
            'userId': item.user_id
        },
    }

    return jsonify(response), 200


@item_api_app.route('/api/items', methods=['POST'])
@auth_enabled(is_required=True)
def add_item(decoded):
    data = request.get_json()

    # validate json

    schema = {
        'name': 'string',
        'description': 'string',
        'categoryId': 'number',
        'required': ['name', 'description', 'categoryId']
    }

    try:
        validate(data, schema)
    except Exception as e:
        raise ValidationError(e.args[0])
        pass

    # validate item name

    valid = Item.validate_slug(slugify(data['name']))

    if not valid:
        raise ValidationError('An item with the same name has already been added. Please try another name.')

    # validate category id

    category = Category.find_by_id(data['categoryId'])

    if category is None:
        raise ValidationError('Invalid category Id')

    item = Item(name=data['name'], description=data['description'], category_id=data['categoryId'],
                user_id=decoded['id'], slug=slugify(data['name']))

    db.session.add(item)
    db.session.commit()

    response = {
        'success': True,
        'data': {
            'id': item.id,
            'name': item.name,
            'slug': item.slug,
            'category': {
                'name': item.category.name,
                'id': item.category.id,
                'slug': item.category.slug
            },
            'description': item.description,
            'userId': item.user_id
        },
    }

    return jsonify(response), 200


@item_api_app.route('/api/items/<int:item_id>', methods=['DELETE'])
@auth_enabled(is_required=True)
def delete_item(item_id, decoded):
    # validate item id

    results = db.session.query(Item).filter_by(id=item_id, user_id=decoded['id']).all()

    if len(results) == 0:
        raise ValidationError('Item not found!')

    item = results[0]

    db.session.delete(item)
    db.session.commit()

    response = {
        'success': True
    }

    return jsonify(response), 200
