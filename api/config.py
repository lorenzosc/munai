import os

from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///patients.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    FHIR_SERVER_URL = os.getenv('FHIR_SERVER_URL', 'http://localhost:8080/baseR4')
    APP_NAME = os.getenv('APP_NAME', 'PatientDataAPI')
    TEMP_DIR = os.getenv('TEMP_DIR', './temp_storage')
