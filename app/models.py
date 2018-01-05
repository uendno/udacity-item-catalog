from app import db
import datetime


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    slug = db.Column(db.String(80), unique=True)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    providerType = db.Column(db.String(80), nullable=False)
    providerId = db.Column(db.String(80), nullable=False)


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.TEXT)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(Category, backref=db.backref('items', lazy=True))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    slug = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User, backref=db.backref('items', lazy=True))

    __table_args__ = (db.UniqueConstraint('category_id', 'slug', name='category_slug_1'),)

    @staticmethod
    def find_by_slug_and_category_slug(item_slug, category_slug):
        return db.session.query(Item, Category) \
            .join(Category.items) \
            .filter(Category.slug == category_slug).filter(Item.slug == item_slug).all()

    @staticmethod
    def find_by_slug_and_category_slug_and_user_id(item_slug, category_slug, user_id):
        return db.session.query(Item, Category) \
            .join(Category.items) \
            .filter(Category.slug == category_slug) \
            .filter(Item.slug == item_slug) \
            .filter_by(slug=item_slug,
                       user_id=user_id) \
            .all()


class GoogleProvider(db.Model):
    __tablename__ = 'google_provider'

    id = db.Column(db.String(80), nullable=False, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    access_token = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    picture = db.Column(db.String(80), nullable=False)
