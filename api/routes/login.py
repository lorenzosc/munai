from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from api.user_service import validate_user_credentials
from datetime import timedelta

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = validate_user_credentials(username, password)
    if not user:
        return jsonify({"msg": "Invalid username or password"}), 401
    
    access_token = create_access_token(identity=user.username, timedelta=timedelta(days=1))
    return jsonify(access_token=access_token), 200