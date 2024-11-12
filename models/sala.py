from extensions import db

class Sala(db.Model):
    __tablename__ = 'sala'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    localizacao = db.Column(db.String(50))
    capacidade = db.Column(db.Integer)
    equipamentos = db.Column(db.String(100))
