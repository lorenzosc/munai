from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PatientData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    genero = db.Column(db.String(10), nullable=False)
    data_nascimento = db.Column(db.DateTime, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    pais_nascimento = db.Column(db.String(50), nullable=False)
    observacao = db.Column(db.String(200), nullable=True)
