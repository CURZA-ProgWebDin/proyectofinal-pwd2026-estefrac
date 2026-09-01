from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .base_model import BaseModel


class Usuario(BaseModel):
    __tablename__ = "usuarios"
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    rol_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    rol = db.relationship("Rol", back_populates="usuarios")
    documentaciones_cargadas = db.relationship(
        "DocumentacionVehiculo",
        foreign_keys="DocumentacionVehiculo.usuario_id",
        back_populates="usuario",
    )
    documentaciones_actualizadas = db.relationship(
        "DocumentacionVehiculo",
        foreign_keys="DocumentacionVehiculo.usuario_actualizacion_id",
        back_populates="usuario_actualizacion",
    )
    asignaciones_creadas = db.relationship(
        "Asignacion", foreign_keys="Asignacion.usuario_id", back_populates="usuario"
    )
    asignaciones_actualizadas = db.relationship(
        "Asignacion",
        foreign_keys="Asignacion.usuario_actualizacion_id",
        back_populates="usuario_actualizacion",
    )
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(
        self, nombre: str, email: str, rol_id: int, password_hash: str
    ) -> None:
        self.nombre = nombre
        self.email = email
        self.rol_id = rol_id
        self.password_hash = password_hash

    def to_dict(self, incluye_rol: bool = False) -> dict:
        data = super().to_dict()
        data.update({"nombre": self.nombre, "email": self.email, "rol_id": self.rol_id})
        if incluye_rol:
            data["rol"] = self.rol.to_dict()
        return data

    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
