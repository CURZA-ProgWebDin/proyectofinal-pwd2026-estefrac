from . import db
from .base_model import BaseModel

class Rol(BaseModel):
    __tablename__ = 'roles'
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    usuarios = db.relationship('Usuario', back_populates='rol')

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "nombre": self.nombre
        })
        return data
