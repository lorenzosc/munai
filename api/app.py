from flask import Flask
from flask_jwt_extended import JWTManager

from api.config import Config
from api.routes import init_app

from api.models import db


app = Flask(__name__)
app.name = Config.APP_NAME
app.config.from_object(Config)

jwt = JWTManager(app)

with app.app_context():
    db.create_all()

init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
