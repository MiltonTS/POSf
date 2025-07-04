import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from .models import Product


def create_app(config=None):
    app = Flask(__name__, template_folder='../templates')
    app.config.update(
        SQLALCHEMY_DATABASE_URI='sqlite:///pos.db',
        SECRET_KEY='dev-secret-key',
    )
    if config:
        app.config.update(config)

    db.init_app(app)

    from . import routes
    app.register_blueprint(routes.bp)

    from .excel import load_products_from_excel

    with app.app_context():
        db.create_all()
        path = app.config.get('LOAD_PRODUCTS_FILE')
        if path and os.path.exists(path) and Product.query.count() == 0:
            # Attempt to populate the database from an Excel sheet
            load_products_from_excel(path)

    return app
