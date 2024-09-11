from flask import Flask, request, jsonify
import pandas as pd
import os
import uuid

app = Flask(__name__)

TEMP_DIR = "./temp_storage"

os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_patients_csv():

    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
    
    df = pd.read_csv(file)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(TEMP_DIR, f"{file_id}.csv")

    df.to_csv(file_path, index=False)

    return jsonify({"file_id": file_id}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
