from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

from config import Config
from routes import init_app


app = Flask(__name__)
app.name = Config.APP_NAME
app.config.from_object(Config)

db = SQLAlchemy(app)
jwt = JWTManager(app)

TEMP_DIR = Config.TEMP_DIR
os.makedirs(TEMP_DIR, exist_ok=True)

with app.app_context():
    db.create_all()

init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
