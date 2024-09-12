from celery import Celery
import pandas as pd
from fhirclient import client
from fhirclient.models.patient import Patient
from fhirclient.models.humanname import HumanName
from fhirclient.models.identifier import Identifier
from fhirclient.models.observation import Observation
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.contactpoint import ContactPoint
import os

from dotenv import load_dotenv
load_dotenv()

app_name = os.getenv('APP_NAME', 'PatientDataAPI')

celery = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'))

settings = {
    'app_id': app_name,
    'api_base': os.getenv('FHIR_SERVER_URL', 'http://localhost:8080/baseR4')
}

@celery.task
def process_csv_data(file_path: str):
    df = pd.read_csv(file_path)
    
    for index, row in df.iterrows():
        process_patient_data(row)

    os.remove(file_path)

def process_patient_data(row):
    smart = client.FHIRClient(settings=settings)
    
    patient = Patient()
    
    patient.name = [HumanName({
        'family': row['Nome'].split()[-1],
        'given': row['Nome'].split()[:-1]
    })]
    
    # TODO: correct the CPF system URL
    patient.identifier = [Identifier({
        'system': 'http://example.org/fhir/sid/cpf',
        'value': row['CPF']
    })]
    
    # TODO verify if 'male' and 'female' is better than 1 and 0
    gender_map = {
        'Masculino': 'male',
        'Feminino': 'female'
    }
    patient.gender = gender_map.get(row['Gênero'].strip(), 'unknown')
    
    patient.birthDate = FHIRDate(row['Data de Nascimento'])
    
    patient.telecom = [ContactPoint({
        'system': 'phone',
        'value': row['Telefone'],
        'use': 'home'
    })]
    
    patient.create(smart.server)
    
    observations = row['Observação'].split('|')
    for obs in observations:
        if obs.strip():
            observation = Observation()
            observation.subject = patient
            observation.code = {
                'coding': [{
                    'system': 'http://snomed.info/sct',
                    'code': 'TODO',  # TODO map the observation code
                    'display': obs.strip()
                }],
                'text': obs.strip()
            }
            observation.status = 'final'
            observation.effectiveDateTime = FHIRDate.today()
            observation.create(smart.server)
