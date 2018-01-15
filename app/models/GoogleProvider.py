from app import db


class GoogleProvider(db.Model):
    """
    GoogleProvider model for storing information of Google account
    """
    __tablename__ = 'google_provider'

    id = db.Column(db.String(80), nullable=False, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    access_token = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    picture = db.Column(db.String(80), nullable=False)
