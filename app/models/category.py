import datetime

from app import db


class CategoryModel(db.Model):
    """
    Category model
    """

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    slug = db.Column(db.String(80), unique=True)

    @staticmethod
    def get_all_categories():
        return db.session.query(CategoryModel).with_entities(CategoryModel.id, CategoryModel.name,
                                                             CategoryModel.slug).all()

    @staticmethod
    def find(category_id=None, slug=None):
        """
        Find category by id
        :param category_id:
        :param slug:
        :return:
        """

        if category_id is not None:
            return db.session.query(CategoryModel).filter_by(id=category_id).one_or_none()
        else:
            return db.session.query(CategoryModel).filter_by(slug=slug).one_or_none()
