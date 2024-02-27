from flask import Flask
from .config import Config

def crate_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app

