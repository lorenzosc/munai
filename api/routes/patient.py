from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import pandas as pd
import os
import uuid
from api.write_to_fhir_task import process_db_data
from api.models import db, PatientData

patient_bp = Blueprint('patient_bp', __name__)

@patient_bp.route('/upload-csv', methods=['POST'])
@jwt_required()
def upload_patients_csv():

    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    df = pd.read_csv(file, encoding='utf-8')
    file_id = str(uuid.uuid4())

    try:
        for _, row in df.iterrows():
            patient = PatientData(
                file_id=file_id,
                nome=row['Nome'],
                cpf=row['CPF'],
                genero=row['Gênero'],
                data_nascimento=row['Data de Nascimento'],
                telefone=row['Telefone'],
                pais_nascimento=row['País de Nascimento'],
                observacao=row['Observação']
            )
            db.session.add(patient)

        db.session.commit()

        process_db_data.delay(file_id)

        return jsonify({"file_id": file_id}), 200
    
    except UnicodeDecodeError:
        db.session.rollback()
        return jsonify({"error": "File encoding error"}), 400
    
    except pd.errors.ParserError:
        db.session.rollback()
        return jsonify({"error": "Failed to parse CSV file"}), 400
    
    except Exception as e:
        return jsonify({"error": f"Unexpected error"}), 500