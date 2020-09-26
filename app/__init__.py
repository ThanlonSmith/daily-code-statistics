from flask import Flask
from app.home import home


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.Config')
    app.register_blueprint(home)
    return app
