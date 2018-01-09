from flask import Blueprint, render_template, session as login_session, request, redirect
from app import db
from app.models import Category, Item
from slugify import slugify

item_app = Blueprint('item_app', __name__,
                     template_folder='templates')


# show item adding page
@item_app.route('/add', methods=['GET'])
def show_add():
    logged_in = login_session.get('access_token') is not None

    if not logged_in:
        return redirect('/login')

    categories = db.session.query(Category)
    return render_template('edit.html', categories=categories, logged_in=logged_in, item=None)


# handle post request for adding an item
@item_app.route('/add', methods=['POST'])
def add():
    logged_in = login_session.get('access_token') is not None

    if not logged_in:
        return redirect('/login')

    name = request.form['title']
    description = request.form['description']
    category_id = request.form['category_id']

    category = Category.find_by_id(category_id)

    if category is None:
        return "Invalid category Id"

    slug = slugify(name)

    if not Item.validate_slug(slug):
        return "Name is already taken"

    new_item = Item(name=name, description=description, category_id=category_id, slug=slug,
                    user_id=login_session.get('id'))

    db.session.add(new_item)
    db.session.commit()
    return redirect('/')


# show an item
@item_app.route('/catalog/<string:category_slug>/<string:item_slug>/<int:item_id>')
def show_item(category_slug, item_slug, item_id):
    # category_slug and item_slug is redundant

    logged_in = login_session.get('access_token') is not None

    item = Item.find_by_id(item_id)

    if item is not None:
        user_id = login_session.get('id')
        return render_template('item.html', logged_in=logged_in, item=item, user_id=user_id)
    else:
        return render_template('404.html', logged_in=logged_in)


# show editing page for an item
@item_app.route('/catalog/<string:category_slug>/<string:item_slug>/<int:item_id>/edit', methods=['GET'])
def show_edit_item(category_slug, item_slug, item_id):
    # category_slug and item_slug is redundant

    logged_in = login_session.get('access_token') is not None

    if not logged_in:
        return redirect('/login')

    item = Item.find_by_id_and_user_id(item_id, login_session.get('id'))

    categories = db.session.query(Category)
    if item is not None:
        return render_template('edit.html', item=item, logged_in=logged_in, categories=categories)
    else:
        return render_template('404.html', logged_in=logged_in)


# handle post request for updating an item
@item_app.route('/catalog/<string:category_slug>/<string:item_slug>/<int:item_id>/edit', methods=['POST'])
def update(category_slug, item_slug, item_id):
    # category_slug and item_slug is redundant

    logged_in = login_session.get('access_token') is not None

    if not logged_in:
        return redirect('/login')

    item = Item.find_by_id_and_user_id(item_id, login_session.get('id'))

    if item is not None:

        valid = Item.validate_slug(slugify(request.form['title']), item.id)

        if not valid:
            return "Name is already taken"

        item.name = request.form['title']
        item.description = request.form['description']
        item.category_id = request.form['category_id']
        item.slug = slugify(item.name)

        category = Category.find_by_id(item.category_id)

        if category is None:
            return "Invalid category Id"

        db.session.add(item)
        db.session.commit()
        return redirect('/')

    else:
        return render_template('404.html', logged_in=logged_in)


# show item-deleting page
@item_app.route('/catalog/<string:category_slug>/<string:item_slug>/<int:item_id>/delete', methods=['GET'])
def show_delete_item(category_slug, item_slug, item_id):
    # category_slug and item_slug is redundant

    logged_in = login_session.get('access_token') is not None

    if not logged_in:
        return redirect('/login')

    item = Item.find_by_id_and_user_id(item_id, login_session.get('id'))

    if item is not None:
        return render_template('delete.html', item=item, logged_in=logged_in)
    else:
        return render_template('404.html', logged_in=logged_in)


# handle post request for deleting an item
@item_app.route('/catalog/<string:category_slug>/<string:item_slug>/<int:item_id>/delete', methods=['POST'])
def delete(category_slug, item_slug, item_id):
    # category_slug and item_slug is redundant

    logged_in = login_session.get('access_token') is not None

    if not logged_in:
        return redirect('/login')

    item = Item.find_by_id_and_user_id(item_id, login_session.get('id'))

    if item is not None:
        db.session.delete(item)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('404.html', logged_in=logged_in)
