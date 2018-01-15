from app import db


class User(db.Model):
    """
    User model
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    providerType = db.Column(db.String(80), nullable=False)
    providerId = db.Column(db.String(80), nullable=False)
