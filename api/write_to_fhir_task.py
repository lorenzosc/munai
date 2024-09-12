from celery import Celery
import pandas as pd
from fhirclient import client
from fhirclient.models.patient import Patient
from fhirclient.models.humanname import HumanName
from fhirclient.models.identifier import Identifier
from fhirclient.models.address import Address
from fhirclient.models.observation import Observation
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.contactpoint import ContactPoint
import os

from api.config import Config
from api.models import db, PatientData

app_name = Config.APP_NAME

celery = Celery('write_to_fhir_task', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

settings = {
    'app_id': app_name,
    'api_base': Config.FHIR_SERVER_URL
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
        'system': 'https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublica.asp',
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
        'value': row['Telefone']
    })]

    patient.address = [Address({
        "country": row['País de Nascimento'],
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
