from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


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

    with app.app_context():
        db.create_all()

    return app
