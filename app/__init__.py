from flask import Flask, jsonify
from flask_cors import CORS
from app.extensions import db
from app.controllers.errors import errors_controller
from app.controllers.category import category_controller
from app.controllers.item import item_controller
from app.controllers.auth import auth_controller

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object('app.config')

# setup db
db.init_app(app)

# setup controllers
app.register_blueprint(category_controller)
app.register_blueprint(item_controller)
app.register_blueprint(auth_controller)
app.register_blueprint(errors_controller)


# general errors handling
@app.errorhandler(404)
def page_not_found(e):
    response = {
        'success': False,
        'message': 'Route not found!'
    }

    return jsonify(response), 404


@app.errorhandler(405)
def page_not_found(e):
    response = {
        'success': False,
        'message': 'Method not allowed'
    }

    return jsonify(response), 405
