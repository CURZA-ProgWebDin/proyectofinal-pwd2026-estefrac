from app.models import db
from app.models.base_model import BaseModel


class TipoDocumentacion(BaseModel):
    __tablename__ = "tipos_documentacion"

    nombre = db.Column(db.String(50), nullable=False, unique=True)
    obligatorio = db.Column(db.Boolean, nullable=False, default=True)
    documentaciones = db.relationship("DocumentacionVehiculo", back_populates="tipo_documentacion")

    def __init__(self, nombre: str, obligatorio: bool) -> None:
        self.nombre = nombre
        self.obligatorio = obligatorio

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "nombre": self.nombre,
            "obligatorio": self.obligatorio
        })
        return data
