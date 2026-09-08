from datetime import date
from decimal import Decimal

from app.models import db
from app.models.base_model import BaseModel


class Mantenimiento(BaseModel):
    __tablename__ = "mantenimientos"

    vehiculo_id = db.Column(db.Integer, db.ForeignKey("vehiculos.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    usuario_actualizacion_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id"), nullable=True
    )
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    fecha_programada = db.Column(db.Date, nullable=True)
    fecha_realizada = db.Column(db.Date, nullable=True)
    uso_registrado = db.Column(db.Integer, nullable=True)
    costo = db.Column(db.Numeric(10, 2), nullable=True)
    estado = db.Column(db.String(20), nullable=False, default="pendiente")
    bloquea_uso = db.Column(db.Boolean, nullable=False, default=False)

    vehiculo = db.relationship("Vehiculo", back_populates="mantenimientos")
    usuario = db.relationship(
        "Usuario", foreign_keys=[usuario_id], back_populates="mantenimientos_creados"
    )
    usuario_actualizacion = db.relationship(
        "Usuario",
        foreign_keys=[usuario_actualizacion_id],
        back_populates="mantenimientos_actualizados",
    )

    def __init__(
        self,
        vehiculo_id: int,
        usuario_id: int,
        tipo: str,
        descripcion: str | None = None,
        fecha_programada: date | None = None,
        fecha_realizada: date | None = None,
        uso_registrado: int | None = None,
        costo: Decimal | None = None,
        estado: str = "pendiente",
        bloquea_uso: bool = False,
        usuario_actualizacion_id: int | None = None,
    ) -> None:
        self.vehiculo_id = vehiculo_id
        self.usuario_id = usuario_id
        self.usuario_actualizacion_id = usuario_actualizacion_id
        self.tipo = tipo
        self.descripcion = descripcion
        self.fecha_programada = fecha_programada
        self.fecha_realizada = fecha_realizada
        self.uso_registrado = uso_registrado
        self.costo = costo
        self.estado = estado
        self.bloquea_uso = bloquea_uso

    def to_dict(self, incluye_relaciones: bool = False) -> dict:
        data = super().to_dict()

        data.update(
            {
                "vehiculo_id": self.vehiculo_id,
                "usuario_id": self.usuario_id,
                "usuario_actualizacion_id": self.usuario_actualizacion_id,
                "tipo": self.tipo,
                "descripcion": self.descripcion,
                "fecha_programada": (
                    self.fecha_programada.isoformat()
                    if self.fecha_programada
                    else None
                ),
                "fecha_realizada": (
                    self.fecha_realizada.isoformat() if self.fecha_realizada else None
                ),
                "uso_registrado": self.uso_registrado,
                "costo": str(self.costo) if self.costo is not None else None,
                "estado": self.estado,
                "bloquea_uso": self.bloquea_uso,
            }
        )

        if incluye_relaciones:
            data["vehiculo"] = self.vehiculo.to_dict()
            data["usuario"] = self.usuario.to_dict()
            data["usuario_actualizacion"] = (
                self.usuario_actualizacion.to_dict()
                if self.usuario_actualizacion
                else None
            )

        return data
