from app import db
from .Category import Category
from .User import User
import datetime


class Item(db.Model):
    """
    Item model
    """

    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.TEXT)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(Category, backref=db.backref('items', lazy=True))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    slug = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User, backref=db.backref('items', lazy=True))

    __table_args__ = (db.UniqueConstraint('category_id', 'slug', name='category_slug_1'),)

    @staticmethod
    def find_by_slug_and_category_slug(item_slug, category_slug):
        """
        Find an item by its slug and its category slug
        :param item_slug: item slug
        :param category_slug: category slug
        :return: an Item or None
        """

        return db.session.query(Item, Category) \
            .join(Category.items) \
            .filter(Category.slug == category_slug).filter(Item.slug == item_slug).all()

    @staticmethod
    def find_by_slug_and_category_slug_and_user_id(item_slug, category_slug, user_id):
        """
        Find an item by its slug, its category slug and its user id
        :param item_slug: item slug
        :param category_slug: category slug
        :param user_id: user id
        :return: an Item or None
        """

        return db.session.query(Item, Category) \
            .join(Category.items) \
            .filter(Category.slug == category_slug) \
            .filter(Item.slug == item_slug) \
            .filter_by(slug=item_slug,
                       user_id=user_id) \
            .all()

    @staticmethod
    def find_by_id(item_id):
        """
        Find an item by its id
        :param item_id: item id
        :return: an Item or None
        """

        results = db.session.query(Item).filter_by(id=item_id).all()

        if len(results) > 0:
            return results[0]
        else:
            return None

    @staticmethod
    def find_by_id_and_user_id(item_id, user_id):
        """
        find an item by its it and its user id
        :param item_id: item id
        :param user_id: user id
        :return: an Item or None
        """

        results = db.session.query(Item).filter_by(id=item_id, user_id=user_id).all()

        if len(results) > 0:
            return results[0]
        else:
            return None

    @staticmethod
    def validate_slug(slug, current_item_id=None):
        """
        Validate an item by its slug
        :param slug: item slug
        :param current_item_id: id of being validated item
        :return: True if valid and False if invalid
        """

        results = db.session.query(Item) \
            .filter(Item.id != current_item_id) \
            .filter_by(slug=slug).all()

        if len(results) > 0:
            return False
        else:
            return True
