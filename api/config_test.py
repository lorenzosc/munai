import os

from dotenv import load_dotenv
load_dotenv(dotenv_path='.env.test')

class Config:
    TESTING = True
    SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    broker_url = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
    result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
    FHIR_SERVER_URL = os.getenv('FHIR_SERVER_URL', 'http://localhost:8080/baseR4')
    APP_NAME = os.getenv('APP_NAME', 'PatientDataAPI')
    TEMP_DIR = os.getenv('TEMP_DIR', './temp_storage')
