from app import db


class User(db.Model):
    """
    User model
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)

    @staticmethod
    def find_by_id(user_id):
        """
        Find an user by id
        :param user_id:
        :return:
        """

        return db.session.query(User).filter_by(id=user_id).one_or_none()
