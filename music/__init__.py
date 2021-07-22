import os

from flask import Flask
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from .routes import authentication, subscription, index
    app.register_blueprint(authentication.bp)
    app.register_blueprint(subscription.bp)
    app.register_blueprint(index.bp)

    from .db import database
    database.init_app(app)

    return app