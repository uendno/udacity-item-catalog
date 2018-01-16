import datetime

from app import db



class Category(db.Model):
    """
    Category model
    """

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    slug = db.Column(db.String(80), unique=True)

    @staticmethod
    def find_by_id(category_id):
        """
        Find category by id
        :param category_id:
        :return:
        """
        return db.session.query(Category).filter_by(id=category_id).one_or_none()

    @staticmethod
    def find_by_slug(slug):
        """
        Find a category by its slug
        :param slug:
        :return:
        """
        return db.session.query(Category).filter_by(slug=slug).one_or_none()
