from app.models import db
from app.models.base_model import BaseModel


class Asignacion(BaseModel):
    __tablename__ = "asignaciones"

    vehiculo_id = db.Column(db.Integer, db.ForeignKey("vehiculos.id"), nullable=False)
    conductor_id = db.Column(
        db.Integer, db.ForeignKey("conductores.id"), nullable=False
    )
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    usuario_actualizacion_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id"), nullable=True
    )
    fecha_salida = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    fecha_regreso = db.Column(db.DateTime, nullable=True)
    uso_salida = db.Column(db.Integer, nullable=False)
    uso_regreso = db.Column(db.Integer, nullable=True)
    destino = db.Column(db.String(150), nullable=True)
    motivo = db.Column(db.Text, nullable=True)
    estado = db.Column(db.String(20), nullable=False, default="abierta")

    vehiculo = db.relationship("Vehiculo", back_populates="asignaciones")
    conductor = db.relationship("Conductor", back_populates="asignaciones")
    usuario = db.relationship(
        "Usuario", foreign_keys=[usuario_id], back_populates="asignaciones_creadas"
    )
    usuario_actualizacion = db.relationship(
        "Usuario",
        foreign_keys=[usuario_actualizacion_id],
        back_populates="asignaciones_actualizadas",
    )

    __table_args__ = (
        db.Index(
            "uq_asignaciones_vehiculo_abierta",
            "vehiculo_id",
            unique=True,
            postgresql_where=db.text("estado = 'abierta'"),
        ),
        db.Index(
            "uq_asignaciones_conductor_abierta",
            "conductor_id",
            unique=True,
            postgresql_where=db.text("estado = 'abierta'"),
        ),
    )

    def __init__(
        self,
        vehiculo_id: int,
        conductor_id: int,
        usuario_id: int,
        uso_salida: int,
        destino: str | None,
        motivo: str | None,
    ) -> None:
        self.vehiculo_id = vehiculo_id
        self.conductor_id = conductor_id
        self.usuario_id = usuario_id
        self.uso_salida = uso_salida
        self.destino = destino
        self.motivo = motivo

    def to_dict(self, incluye_relaciones: bool = False) -> dict:
        data = super().to_dict()

        data.update(
            {
                "vehiculo_id": self.vehiculo_id,
                "conductor_id": self.conductor_id,
                "usuario_id": self.usuario_id,
                "usuario_actualizacion_id": self.usuario_actualizacion_id,
                "fecha_salida": (
                    self.fecha_salida.isoformat() if self.fecha_salida else None
                ),
                "fecha_regreso": (
                    self.fecha_regreso.isoformat() if self.fecha_regreso else None
                ),
                "uso_salida": self.uso_salida,
                "uso_regreso": self.uso_regreso,
                "destino": self.destino,
                "motivo": self.motivo,
                "estado": self.estado,
            }
        )

        if incluye_relaciones:
            data["vehiculo"] = self.vehiculo.to_dict()
            data["conductor"] = self.conductor.to_dict()
            data["usuario"] = self.usuario.to_dict()
            data["usuario_actualizacion"] = (
                self.usuario_actualizacion.to_dict()
                if self.usuario_actualizacion
                else None
            )

        return data
