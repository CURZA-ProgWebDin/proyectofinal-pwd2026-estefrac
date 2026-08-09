from . import db
from .base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(BaseModel):
    __tablename__ = 'usuarios'
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    rol = db.relationship('Rol', back_populates='usuarios')
    password_hash = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.String(1), nullable=False, default='S')

    def __init__(self, nombre: str, email:str, rol_id: int, password_hash:str) -> None:
        self.nombre = nombre
        self.email = email
        self.rol_id = rol_id
        self.password_hash = password_hash

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "nombre": self.nombre,
            "email": self.email,
            "rol_id": self.rol_id,
            "activo": self.activo
        })
        return data

    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
