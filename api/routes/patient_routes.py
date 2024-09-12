from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import pandas as pd
import os
import uuid
from api.tasks import process_csv_data
from api.config import Config

TEMP_DIR = Config.TEMP_DIR

patient_bp = Blueprint('patient_bp', __name__)

@patient_bp.route('/upload-csv', methods=['POST'])
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