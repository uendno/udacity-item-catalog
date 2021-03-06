import datetime

from app import db
from .category import CategoryModel
from .user import UserModel


class ItemModel(db.Model):
    """
    Item model
    """

    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.TEXT)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(CategoryModel, backref=db.backref('items', lazy=True))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    slug = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(UserModel, backref=db.backref('items', lazy=True))

    __table_args__ = (db.UniqueConstraint('slug', name='slug_unique_1'),)

    @staticmethod
    def find(item_id):
        """
        Find an item by its id
        :param item_id: item id
        :return: an Item or None
        """

        return db.session.query(ItemModel).filter_by(id=item_id).one_or_none()

    @staticmethod
    def get_user_item(item_id, user_id):
        """
        Find an item by its it and its user id
        :param item_id: item id
        :param user_id: user id
        :return: an Item or None
        """

        return db.session.query(ItemModel).filter_by(id=item_id, user_id=user_id).one_or_none()

    @staticmethod
    def validate_slug(slug):
        """
        Validate an item by its slug
        :param slug: item slug
        :return: True if valid and False if invalid
        """

        item = db.session.query(ItemModel) \
            .filter_by(slug=slug).one_or_none()

        if item is not None:
            return False
        else:
            return True

    @staticmethod
    def get_last_n_items(n=10):
        return db.session.query(ItemModel).order_by(ItemModel.created_date.desc()).limit(n).all()

    @staticmethod
    def get_all_items():
        return db.session.query(ItemModel).all()
