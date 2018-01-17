from flask_script import Manager
from app import app, db
from app.models import Category
from slugify import slugify

manager = Manager(app)


# initialize database
@manager.command
def init_db():
    db.create_all()


# seed categories
@manager.command
def seed_categories():
    categories_names = ['Soccer', 'Basketball', 'Baseball', 'Frisbee', 'Snowboarding', 'Rock Climbing', 'Foosball',
                        'Skating', 'Hockey']
    categories = map(lambda name: Category(name=name, slug=slugify(name)), categories_names)
    db.session.bulk_save_objects(categories)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
