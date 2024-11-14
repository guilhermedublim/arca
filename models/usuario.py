from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(100), nullable=False, unique=True)
    tipo_usuario = db.Column(db.String(10), nullable=False, default='NORMAL')
    senha = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, senha):
        self.senha = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha, senha)