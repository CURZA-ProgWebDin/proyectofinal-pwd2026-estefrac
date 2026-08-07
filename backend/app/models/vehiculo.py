from app.models.base_model import BaseModel
from app.models import db

class Vehiculo(BaseModel):
    __tablename__ = "vehiculos"

    patente = db.Column(db.String(20), unique=True, nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    tipo_vehiculo_id = db.Column(db.Integer, db.ForeignKey("tipos_vehiculos.id"), nullable=False)
    uso_actual = db.Column(db.Integer, nullable=False, default=0)
    estado = db.Column(db.String(30), nullable=False, default="disponible")
    activo = db.Column(db.String(1), nullable=False, default="S")

    tipo_vehiculo = db.relationship("TipoVehiculo", back_populates="vehiculos")

    def __init__(self, patente: str, marca: str, modelo: str, anio: int, tipo_vehiculo_id: int, uso_actual:int) -> None:
        self.patente = patente
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.tipo_vehiculo_id = tipo_vehiculo_id
        self.uso_actual = uso_actual

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "patente": self.patente,
            "marca": self.marca,
            "modelo": self.modelo,
            "anio": self.anio,
            "tipo_vehiculo_id": self.tipo_vehiculo_id,
            "uso_actual": self.uso_actual,
            "estado": self.estado,
            "activo": self.activo
        })
        return data
