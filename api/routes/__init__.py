from flask import Blueprint
from api.routes.patient import patient_bp
from api.routes.login import login_bp

def init_app(app):
    app.register_blueprint(patient_bp)
    app.register_blueprint(login_bp)