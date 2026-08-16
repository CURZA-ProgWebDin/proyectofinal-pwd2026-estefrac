from app.models.base_model import BaseModel
from app.models import db
from datetime import date


class Conductor(BaseModel):
    __tablename__ = "conductores"

    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), nullable=False, unique=True)
    telefono = db.Column(db.String(30), nullable=False)
    licencia_numero = db.Column(db.String(50), nullable=False, unique=True)
    licencia_vencimiento = db.Column(db.Date, nullable=False)
    activo = db.Column(db.String(1), nullable=False, default="S")

    def __init__(
        self,
        nombre: str,
        apellido: str,
        dni: str,
        telefono: str,
        licencia_numero: str,
        licencia_vencimiento: date
    ) -> None:
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.telefono = telefono
        self.licencia_numero = licencia_numero
        self.licencia_vencimiento = licencia_vencimiento

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "telefono": self.telefono,
            "licencia_numero": self.licencia_numero,
            "licencia_vencimiento": (self.licencia_vencimiento.isoformat() if self.licencia_vencimiento else None),
            "activo": self.activo
        })
        return data
