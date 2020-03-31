from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_object='config.Config'):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_object)

    with app.app_context():
        db.init_app(app)
        from . import routes  # noqa: F401
        return app
