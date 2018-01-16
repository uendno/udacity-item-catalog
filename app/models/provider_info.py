from app import db
from .user import User


class ProviderInfo(db.Model):
    """
    GoogleProvider model for storing information of Google account
    """
    __tablename__ = 'provider_info'

    id = db.Column(db.String(80), nullable=False, primary_key=True)
    type = db.Column(db.String(20), nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User, backref=db.backref('provider_infos', lazy=True))
    email = db.Column(db.String(80), nullable=False)
    access_token = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    picture = db.Column(db.String(80), nullable=False)

    @staticmethod
    def find_by_id_and_type(provider_id, provider_type):
        """
        Find an provider info by its id and type
        :param provider_id:
        :param provider_type:
        :return:
        """
        return db.session.query(ProviderInfo).filter_by(id=provider_id, type=provider_type).one_or_none()
