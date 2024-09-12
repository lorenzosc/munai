from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    # TODO: Add user authentication logic with SQLAlchemy
    access_token = create_access_token(identity=data['username'], expires_delta=timedelta(days=1))
    return jsonify(access_token=access_token)