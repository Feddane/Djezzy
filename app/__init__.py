from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from .config import Config

db = SQLAlchemy()

def create_app():
    upload_dir = 'app/static/uploads'
    os.makedirs(upload_dir, exist_ok=True)

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    return app
