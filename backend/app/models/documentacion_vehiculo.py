from app.models.base_model import BaseModel
from app.models import db
from datetime import date

class DocumentacionVehiculo(BaseModel):
    __tablename__ = "documentacion_vehiculos"

    vehiculo_id = db.Column(db.Integer, db.ForeignKey("vehiculos.id"), nullable=False)
    tipo_documentacion_id = db.Column(db.Integer, db.ForeignKey("tipos_documentacion.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    usuario_actualizacion_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    numero = db.Column(db.String(100), nullable=True)
    fecha_emision = db.Column(db.Date, nullable=True)
    fecha_vencimiento = db.Column(db.Date, nullable=False)
    vehiculo = db.relationship("Vehiculo", back_populates="documentaciones")
    tipo_documentacion = db.relationship("TipoDocumentacion", back_populates="documentaciones")
    usuario = db.relationship("Usuario", foreign_keys=[usuario_id], back_populates="documentaciones_cargadas")
    usuario_actualizacion = db.relationship("Usuario", foreign_keys=[usuario_actualizacion_id], back_populates="documentaciones_actualizadas")


    def __init__(self, vehiculo_id: int, tipo_documentacion_id: int, usuario_id: int, numero: str | None, fecha_emision: date | None, fecha_vencimiento: date, usuario_actualizacion_id: int | None = None) -> None:
        self.vehiculo_id = vehiculo_id
        self.tipo_documentacion_id = tipo_documentacion_id
        self.usuario_id = usuario_id
        self.usuario_actualizacion_id = usuario_actualizacion_id
        self.numero = numero
        self.fecha_emision = fecha_emision
        self.fecha_vencimiento = fecha_vencimiento
    def to_dict(self, incluye_tipo_documentacion: bool = False) -> dict:
        data = super().to_dict()
        data.update({
            "vehiculo_id": self.vehiculo_id,
            "tipo_documentacion_id": self.tipo_documentacion_id,
            "usuario_id": self.usuario_id,
            "usuario_actualizacion_id": self.usuario_actualizacion_id,
            "numero": self.numero,
            "fecha_emision": (
                self.fecha_emision.isoformat()
                if self.fecha_emision
                else None
            ),
            "fecha_vencimiento": (
                self.fecha_vencimiento.isoformat()
                if self.fecha_vencimiento
                else None
            )
        })

        if incluye_tipo_documentacion:
            data["tipo_documentacion"] = self.tipo_documentacion.to_dict()

        return data
