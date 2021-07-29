import os

from flask import Flask
from flask_login import login_manager, login_user, logout_user, login_required, current_user, LoginManager

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    loginManager = LoginManager(app)
    loginManager.login_view = 'authentication/login'

    from .routes import authentication, subscription, index
    app.register_blueprint(authentication.bp)
    app.register_blueprint(subscription.bp)
    app.register_blueprint(index.bp)

    from .db import dynamodb, s3
    dynamodb.init_app(app)
    s3.init_app(app)    

    @loginManager.user_loader
    def load_user(id):
        return dynamodb.get_user(id)

    return app