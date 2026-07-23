from . import db
from .base_model import BaseModel

class Rol(BaseModel):
    __tablename__ = 'roles'
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    activo = db.Column(db.String(1), nullable=False, default='S')
    usuarios = db.relationship('Usuario', back_populates='rol')

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "nombre": self.nombre,
            "activo": self.activo
        })
        return data
