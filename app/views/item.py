from flask import Blueprint, render_template, session as login_session, request, redirect
from app import db
from app.models import Category, Item
from slugify import slugify

item_app = Blueprint('item_app', __name__,
                     template_folder='templates')


@item_app.route('/catalog/<string:category_slug>/<string:item_slug>')
def item(category_slug, item_slug):
    logged_in = login_session.get('access_token') is not None
    items = Item.find_by_slug_and_category_slug(item_slug, category_slug)

    if len(items) > 0:
        user_id = login_session.get('id')
        return render_template('item.html', logged_in=logged_in, item=items[0][0], user_id=user_id)
    else:
        return render_template('404.html', logged_in=logged_in)


@item_app.route('/catalog/<string:category_slug>/<string:item_slug>/edit', methods=['GET'])
def showEditItem(category_slug, item_slug):
    logged_in = login_session.get('access_token') is not None

    if not logged_in:
        return redirect('/login')

    items = Item.find_by_slug_and_category_slug_and_user_id(item_slug, category_slug, login_session.get(
        'id'))

    categories = db.session.query(Category)
    if len(items) > 0:
        return render_template('edit.html', item=items[0][0], logged_in=logged_in, categories=categories)
    else:
        return render_template('404.html', logged_in=logged_in)


@item_app.route('/add', methods=['GET'])
def showAdd():
    logged_in = login_session.get('access_token') is not None

    if not logged_in:
        return redirect('/login')

    categories = db.session.query(Category)
    return render_template('edit.html', categories=categories, logged_in=logged_in, item=None)


@item_app.route('/add', methods=['POST'])
def add():
    logged_in = login_session.get('access_token') is not None

    if not logged_in:
        return redirect('/login')

    name = request.form['title']
    description = request.form['description']
    category_id = request.form['category_id']

    new_item = Item(name=name, description=description, category_id=category_id, slug=slugify(name),
                    user_id=login_session.get('id'))
    try:
        db.session.add(item)
        db.session.commit()
        return redirect('/')
    except:
        return "Invalid item name"

    return redirect('/')


@item_app.route('/catalog/<string:category_slug>/<string:item_slug>/edit', methods=['POST'])
def update(category_slug, item_slug):
    logged_in = login_session.get('access_token') is not None

    if not logged_in:
        return redirect('/login')

    items = Item.find_by_slug_and_category_slug_and_user_id(item_slug, category_slug, login_session.get(
        'id'))

    if len(items) > 0:
        item = items[0][0]
        item.name = request.form['title']
        item.description = request.form['description']
        item.category_id = request.form['category_id']

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Invalid item name"

    else:
        return render_template('404.html', logged_in=logged_in)


@item_app.route('/catalog/<string:category_slug>/<string:item_slug>/delete', methods=['GET'])
def showDeleteItem(category_slug, item_slug):
    logged_in = login_session.get('access_token') is not None

    if not logged_in:
        return redirect('/login')

    items = Item.find_by_slug_and_category_slug_and_user_id(item_slug, category_slug, login_session.get(
        'id'))

    if len(items) > 0:
        return render_template('delete.html', item=items[0][0], logged_in=logged_in)
    else:
        return render_template('404.html', logged_in=logged_in)


@item_app.route('/catalog/<string:category_slug>/<string:item_slug>/delete', methods=['POST'])
def delete(category_slug, item_slug):
    logged_in = login_session.get('access_token') is not None

    if not logged_in:
        return redirect('/login')

    items = Item.find_by_slug_and_category_slug_and_user_id(item_slug, category_slug, login_session.get(
        'id'))

    if len(items) > 0:
        db.session.delete(items[0][0])
        db.session.commit()
        return redirect('/')
    else:
        return render_template('404.html', logged_in=logged_in)
