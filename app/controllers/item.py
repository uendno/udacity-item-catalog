from jsonschema import validate
from slugify import slugify
from flask import Blueprint, jsonify, request

from app import db
from app.models import ItemModel, CategoryModel
from app.models.errors import ValidationError
from app.helpers.decorators import auth_enabled
from app.helpers.response import send_success
from app.schemas import ItemSchema

item_controller = Blueprint('item_controller', __name__)


@item_controller.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """
    Get details for an item. Find by its id
    :param item_id: item id
    :return:
    """

    item = ItemModel.find(item_id)

    if item is None:
        raise ValidationError('Item not found!')

    item_schema = ItemSchema()
    result = item_schema.dump(item)

    return send_success(result.data)


@item_controller.route('/items')
def get_items():
    """
    Get a list of items
    :return:
    """

    mode = request.args.get('mode')
    limit = request.args.get('limit')

    if mode == 'latest':
        items = ItemModel.get_last_n_items(limit)
    else:
        items = ItemModel.get_all_items()

    items_schema = ItemSchema(many=True, load_only=('user_id', 'description',))
    result = items_schema.dump(items)

    return send_success(result.data)


@item_controller.route('/items/<int:item_id>', methods=['PUT'])
@auth_enabled(is_required=True)
def update_item(item_id, user_info):
    """
    Update an item, find by its id
    Protected
    :param item_id: item id
    :param user_info: decoded access token
    :return:
    """

    data = request.get_json()

    # Validate json
    schema = ItemSchema(dump_only=('slug',))
    errors = schema.validate(data)
    if len(errors) > 0:
        raise ValidationError('Post data error', errors)

    # Validate item id
    item = ItemModel.get_user_item(item_id, user_info.get('id'))
    if item is None:
        raise ValidationError('Item not found!')

    # Validate item name
    slug = slugify(data['name'])
    if slug != item.slug:
        valid = ItemModel.validate_slug(slug)

        if not valid:
            raise ValidationError('An item with the same name has already been added. Please try another name.')

    # Validate category id
    category = CategoryModel.find(category_id=data['category_id'])
    if category is None:
        raise ValidationError('Invalid category Id')

    item.name = data['name']
    item.description = data['description']
    item.category_id = data['category_id']
    item.slug = slugify(item.name)

    db.session.add(item)
    db.session.commit()

    item_schema = ItemSchema()
    result = item_schema.dump(item)

    return send_success(result.data)


@item_controller.route('/items', methods=['POST'])
@auth_enabled(is_required=True)
def create_item(user_info):
    """
    Add an item
    Protected
    :param user_info: decoded access token
    :return:
    """

    data = request.get_json()

    # Validate json
    schema = ItemSchema(dump_only=('slug', 'id'))
    errors = schema.validate(data)
    if len(errors) > 0:
        raise ValidationError('Post data error', errors)

    # Validate item name
    valid = ItemModel.validate_slug(slugify(data['name']))

    if not valid:
        raise ValidationError('An item with the same name has already been added. Please try another name.')

    # Validate category id
    category = CategoryModel.find(category_id=data['category_id'])

    if category is None:
        raise ValidationError('Invalid category Id')

    item = ItemModel(name=data['name'], description=data['description'], category_id=data['category_id'],
                     user_id=user_info['id'], slug=slugify(data['name']))

    db.session.add(item)
    db.session.commit()

    item_schema = ItemSchema()
    result = item_schema.dump(item)

    return send_success(result.data)


@item_controller.route('/items/<int:item_id>', methods=['DELETE'])
@auth_enabled(is_required=True)
def delete_item(item_id, user_info):
    """
    Delete an item, find by its id
    Protected
    :param item_id: item id
    :param user_info: decoded access token
    :return:
    """

    # Validate item id
    item = ItemModel.get_user_item(item_id, user_info.get('id'))

    if item is None:
        raise ValidationError('Item not found!')

    db.session.delete(item)
    db.session.commit()

    return send_success(None)
