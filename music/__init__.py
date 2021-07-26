import os

from flask import Flask
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    from .routes import authentication, subscription, index
    app.register_blueprint(authentication.bp)
    app.register_blueprint(subscription.bp)
    app.register_blueprint(index.bp)

    from .db import dynamodb, s3
    dynamodb.init_app(app)
    s3.init_app(app)

    return app