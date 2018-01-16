from flask import Blueprint

from app import db
from app.models import Category, Item
from app.models.errors import ValidationError
from app.helpers.response import send_success

category_controller = Blueprint('category_controller', __name__)


@category_controller.route('/categories')
def get_categories():
    """
    Get all categories
    :return: Response contains list of categories
    """

    categories = db.session.query(Category)

    data = []

    for category in categories:
        data.append({
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
        })

    return send_success(data)


@category_controller.route('/categories/<string:category_slug>')
def get_category(category_slug):
    """
    Get details for a category. Find by its slug
    :param category_slug: category slug
    :return: Response details for that categories, including its items
    """

    category = Category.find_by_slug(category_slug)

    if category is None:
        raise ValidationError('Category not found!')

    items = category.items

    data = {
        'id': category.id,
        'name': category.name,
        'slug': category.slug,
        'items': []
    }

    for item in items:
        data['items'].append({
            'id': item.id,
            'name': item.name,
            'slug': item.slug,
            'category': {
                'name': item.category.name,
                'id': item.category.id,
                'slug': item.category.slug
            }
        })

    return send_success(data)
