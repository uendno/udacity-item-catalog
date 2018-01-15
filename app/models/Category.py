from app import db
import datetime


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
        results = db.session.query(Category).filter_by(id=category_id).all()

        if len(results) > 0:
            return results[0]
        else:
            return None
