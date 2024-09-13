from celery import Celery
import logging

from fhirclient import client
from fhirclient.models.patient import Patient
from fhirclient.models.humanname import HumanName
from fhirclient.models.identifier import Identifier
from fhirclient.models.address import Address
from fhirclient.models.observation import Observation
from fhirclient.models.condition import Condition
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.contactpoint import ContactPoint

from api.snomed_ct import SnomedCtExample
snomed = SnomedCtExample()

from api.config import Config
from api.models import db, PatientData

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app_name = Config.APP_NAME
celery = Celery('write_to_fhir_task', broker=Config.broker_url, backend=Config.result_backend)
celery.config_from_object(Config)

settings = {
    'app_id': app_name,
    'api_base': Config.FHIR_SERVER_URL
}

@celery.task
def process_db_data(file_path: str):
    logger.info(f'Starting to process data for file: {file_path}')
    patients = PatientData.query.filter_by(file_id=file_path).all()
    
    for patient in patients:
        try:
            process_patient_data(patient)
            logger.info(f'Successfully processed patient: {patient.nome}')
            db.session.delete(patient)
        except Exception as e:
            logger.error(f'Error processing patient {patient.nome}: {e}')
    
    db.session.commit()

    logger.info(f'Finished processing data for file: {file_path}')


def process_patient_data(row):
    smart = client.FHIRClient(settings=settings)
    
    patient = Patient()
    
    names = row.nome.split()
    patient.name = [HumanName({
        'family': names[-1],
        'given': names[:-1]
    })]
    
    patient.identifier = [Identifier({
        'system': 'https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublica.asp',
        'value': row.cpf
    })]
    
    gender_map = {
        'Masculino': 'male',
        'Feminino': 'female'
    }
    patient.gender = gender_map.get(row.genero.strip(), 'unknown')
    
    patient.birthDate = FHIRDate(row.data_nascimento)
    
    patient.telecom = [ContactPoint({
        'system': 'phone',
        'value': row.telefone
    })]

    patient.address = [Address({
        "country": row.pais_nascimento,
    })]
    
    patient.create(smart.server)
    logger.info(f'Created FHIR patient resource for {row.nome}')
    
    observations = row.observacao.split('|')
    for observation in observations:
        obs = observation.strip()
        if obs:
            if snomed.check_observation(obs):
                observation = Observation()
                observation.subject = patient
                observation.code = {
                    'coding': [{
                        'system': 'http://snomed.info/sct',
                        'code': snomed.get_code_from_name(obs),
                        'display': obs
                    }],
                    'text': obs
                }
                observation.status = 'final'
                observation.effectiveDateTime = FHIRDate.today()
                observation.create(smart.server)
                logger.info(f'Created FHIR observation resource {obs} for {row.nome}')

            else:
                condition = Condition()
                condition.subject = patient
                condition.code = {
                    'coding': [{
                        'system': 'http://snomed.info/sct',
                        'code': snomed.get_code_from_name(obs),
                        'display': obs
                    }],
                    'text': obs
                }
                condition.onsetDateTime = FHIRDate.today()
                condition.create(smart.server)
                logger.info(f'Created FHIR condition resource {obs} for {row.nome}')
