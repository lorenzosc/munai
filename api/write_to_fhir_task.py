from api.celery_app import celery
import logging

from datetime import datetime, timezone

from fhirclient import client
from fhirclient.models.patient import Patient
from fhirclient.models.humanname import HumanName
from fhirclient.models.identifier import Identifier
from fhirclient.models.address import Address
from fhirclient.models.observation import Observation
from fhirclient.models.condition import Condition
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.fhirdatetime import FHIRDateTime
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding

from api.snomed_ct import SnomedCtExample
snomed = SnomedCtExample()

from api.config import Config
from api.models import db, PatientData

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app_name = Config.APP_NAME

settings = {
    'app_id': app_name,
    'api_base': 'http://fhir-server:8080/fhir'
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
    
    patient.birthDate = FHIRDate(row.data_nascimento.strftime('%Y-%m-%d'))
    
    patient.telecom = [ContactPoint({
        'system': 'phone',
        'value': row.telefone
    })]

    patient.address = [Address({
        "country": row.pais_nascimento,
    })]
    
    patient = patient.create(smart.server)
    logger.info(f'Created FHIR patient resource for {row.nome}')
    
    if row.observacao:
        observations = row.observacao.split('|')
        for observation in observations:
            obs = observation.strip()
            if obs:
                if snomed.check_observation(obs):
                    
                    observation = Observation()
                    observation.code = CodeableConcept()
                    observation.code.coding = [Coding({
                            'system': 'http://snomed.info/sct',
                            'code': snomed.get_code_from_name(obs),
                            'display': obs
                        })]
                    observation.code.text = obs
                    observation.status = 'final'
                    observation.effectiveDateTime = FHIRDateTime(datetime.now(timezone.utc).replace(microsecond=0).isoformat())
                    observation.subject = FHIRReference({'reference': f'Patient/{patient["id"]}'})

                    observation.create(smart.server)
                    logger.info(f'Created FHIR observation resource {obs} for {row.nome}')

                else:
                    condition = Condition()
                    condition.subject = FHIRReference({'reference': f'Patient/{patient["id"]}'})
                    condition.code = CodeableConcept()
                    condition.code.coding = [Coding({
                        'system': 'http://snomed.info/sct',
                        'code': snomed.get_code_from_name(obs),
                        'display': obs
                    })]
                    condition.code.text = obs
                    condition.onsetDateTime = FHIRDateTime(datetime.now(timezone.utc).replace(microsecond=0).isoformat())
                    condition.create(smart.server)
                    logger.info(f'Created FHIR condition resource {obs} for {row.nome}')
