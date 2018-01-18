from flask import Blueprint

from app.models import CategoryModel
from app.models.errors import ValidationError
from app.helpers.response import send_success
from app.schemas import CategorySchema

category_controller = Blueprint('category_controller', __name__)


@category_controller.route('/categories')
def get_categories():
    """
    Get all categories
    :return: Response contains list of categories
    """

    categories = CategoryModel.get_all_categories()

    categories_schema = CategorySchema(many=True)
    result = categories_schema.dump(categories)

    return send_success(result.data)


@category_controller.route('/categories/<string:category_slug>')
def get_category(category_slug):
    """
    Get details for a category. Find by its slug
    :param category_slug: category slug
    :return: Response details for that categories, including its items
    """

    category = CategoryModel.find(slug=category_slug)

    if category is None:
        raise ValidationError('Category not found!')

    category_schema = CategorySchema(load_only=('items.description', 'items.user_id',))
    result = category_schema.dump(category)

    return send_success(result.data)
