from app.models.base_model import BaseModel
from app.models import db

class TipoVehiculo(BaseModel):
    __tablename__ = "tipos_vehiculos"

    nombre = db.Column(db.String(50), unique=True, nullable=False)
    unidad_uso = db.Column(db.String(20), nullable=False)
    vehiculos = db.relationship("Vehiculo", back_populates="tipo_vehiculo")

    def __init__(self, nombre: str, unidad_uso: str) -> None:
        self.nombre = nombre
        self.unidad_uso = unidad_uso

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "nombre": self.nombre,
            "unidad_uso": self.unidad_uso
        })
        return data
