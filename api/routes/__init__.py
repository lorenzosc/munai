from flask import Blueprint
from .patient_routes import patient_bp
from .login import login_bp

def init_app(app):
    app.register_blueprint(patient_bp)
    app.register_blueprint(login_bp)