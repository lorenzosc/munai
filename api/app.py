from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import pandas as pd
import os
import uuid
from datetime import timedelta

from tasks import process_csv_data

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.name = os.getenv('APP_NAME', 'PatientDataAPI')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///test.db')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')

TEMP_DIR = os.getenv('TEMP_DIR', './temp_storage')

db = SQLAlchemy(app)
jwt = JWTManager(app)

os.makedirs(TEMP_DIR, exist_ok=True)

with app.app_context():
    db.create_all()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    # TODO: Add user authentication logic with SQLAlchemy
    access_token = create_access_token(identity=data['username'], expires_delta=timedelta(days=1))
    return jsonify(access_token=access_token)

@app.route('/upload-csv', methods=['POST'])
@jwt_required()
def upload_patients_csv():

    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400
    

    # TODO change this to a more secure way to read the file using SQLAlchemy
    df = pd.read_csv(file)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(TEMP_DIR, f"{file_id}.csv")

    df.to_csv(file_path, index=False)

    process_csv_data.delay(file_path)

    return jsonify({"file_id": file_id}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
