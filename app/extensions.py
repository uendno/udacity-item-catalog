import logging

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Setup database
db = SQLAlchemy()


def enable_cors(app):
    """
    Set up CORS
    :param app:
    :return:
    """
    CORS(app, resources={'*': {'origins': '*'}})


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
