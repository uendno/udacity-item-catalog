from app import db
from .user import UserModel


class OpenAuthenticationModel(db.Model):
    """
    GoogleProvider model for storing information of Google account
    """
    __tablename__ = 'open_authentication'

    id = db.Column(db.String(80), nullable=False, primary_key=True)
    type = db.Column(db.String(20), nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(UserModel, backref=db.backref('open_authentications', lazy=True))

    @staticmethod
    def find(oauth_id, oauth_type):
        """
        Find an provider info by its id and type
        :param oauth_id:
        :param oauth_type:
        :return:
        """
        return db.session.query(OpenAuthenticationModel).filter_by(id=oauth_id, type=oauth_type).one_or_none()
