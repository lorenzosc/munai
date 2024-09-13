from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from api.config import Config

from api.models import db

def create_app():
    app = Flask(__name__)
    app.name = Config.APP_NAME
    app.config.from_object(Config)

    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app