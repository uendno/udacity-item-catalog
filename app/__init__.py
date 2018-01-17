from flask import Flask, jsonify

from app.extensions import db, enable_cors
from app.controllers.errors import errors_controller
from app.controllers.category import category_controller
from app.controllers.item import item_controller
from app.controllers.auth import auth_controller

app = Flask(__name__)
app.config.from_object('app.config')

# Setup db
db.init_app(app)

# Setup CORS
enable_cors(app)

# Setup controllers
app.register_blueprint(category_controller)
app.register_blueprint(item_controller)
app.register_blueprint(auth_controller)
app.register_blueprint(errors_controller)


# General errors handling
@app.errorhandler(404)
def page_not_found(e):
    response = {
        'success': False,
        'message': 'Route not found!'
    }

    return jsonify(response), 404


@app.errorhandler(405)
def method_not_allowed(e):
    response = {
        'success': False,
        'message': 'Method not allowed'
    }

    return jsonify(response), 405
