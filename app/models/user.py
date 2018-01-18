from app import db


class UserModel(db.Model):
    """
    User model
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)

    @staticmethod
    def find(user_id):
        """
        Find an user by id
        :param user_id:
        :return:
        """

        return db.session.query(UserModel).filter_by(id=user_id).one_or_none()
