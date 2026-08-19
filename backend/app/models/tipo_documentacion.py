from app.models.base_model import BaseModel
from app.models import db

class TipoDocumentacion(BaseModel):
    __tablename__ = "tipos_documentacion"

    nombre = db.Column(db.String(50), nullable=False, unique=True)
    obligatorio = db.Column(db.Boolean, nullable=False, default=True)
    activo = db.Column(db.String(1), nullable=False, default="S")

    def __init__(self, nombre: str, obligatorio: bool) -> None:
        self.nombre = nombre
        self.obligatorio = obligatorio

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "nombre": self.nombre,
            "obligatorio": self.obligatorio,
            "activo": self.activo
        })
        return data
