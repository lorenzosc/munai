from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from api.config import Config
from api.routes import init_app

from api.models import db


app = Flask(__name__)
app.name = Config.APP_NAME
app.config.from_object(Config)

jwt = JWTManager(app)
migrate = Migrate(app, db)

init_app(app)

db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
