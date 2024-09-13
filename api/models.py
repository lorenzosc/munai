from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class PatientData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.String(36), nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    genero = db.Column(db.String(10), nullable=False)
    data_nascimento = db.Column(db.DateTime, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    pais_nascimento = db.Column(db.String(50), nullable=False)
    observacao = db.Column(db.String(200), nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)