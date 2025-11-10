import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .logging_config import setup_logging

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Check the environment from the FLASK_ENV
    env = os.environ.get('FLASK_ENV', 'test')
    if env == 'prod':
        app.config.from_object('ManualTestFiller.config.ProdConfig')
    elif env == 'dev':
        app.config.from_object('ManualTestFiller.config.DevConfig')
    else:
        app.config.from_object('ManualTestFiller.config.TestConfig')

    db.init_app(app=app)
    setup_logging(app=app)

    app.logger.info(f"Running in DEBUG={app.config['DEBUG']}")

    with app.app_context():
        from .routes.user import user_bp
        app.register_blueprint(user_bp)
        db.create_all()

    return app
