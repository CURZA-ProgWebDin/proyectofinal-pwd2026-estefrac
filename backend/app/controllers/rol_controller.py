from app.controllers import Controller
from app.models import db
from app.models.rol import Rol
from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError

class RolController(Controller):
    @staticmethod
    def get_all() -> tuple[Response, int]:
        roles = db.session.execute(db.select(Rol).order_by(db.desc(Rol.id))).scalars().all()

        if roles:
            return jsonify([rol.to_dict() for rol in roles]), 200

        return jsonify({"message": "Roles no encontrados"}), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        rol = db.session.get(Rol, id)

        if rol:
            return jsonify(rol.to_dict()), 200

        return jsonify({"message": "Rol no encontrado"}), 404

    @staticmethod
    def create(request: dict) -> tuple[Response, int]:
        nombre: str | None = request.get("nombre")

        if nombre is None:
            return jsonify({"message": "El nombre es requerido"}), 422

        try:
            rol = Rol(nombre=nombre)
            db.session.add(rol)
            db.session.commit()

            return jsonify({"message": "Rol creado exitosamente"}), 201

        except IntegrityError:
            db.session.rollback()

            return jsonify({"message": "El nombre del rol ya existe"}), 409

    @staticmethod
    def update(request: dict, id: int) -> tuple[Response, int]:
        nombre: str | None = request.get("nombre")
        activo: str | None = request.get("activo")

        if nombre is None:
            return jsonify({"message": "El nombre es requerido"}), 422

        if activo is None:
            return jsonify({"message": "El estado activo es requerido"}), 422

        if activo not in ["S", "N"]:
            return jsonify({"message": "El estado activo debe ser 'S' o 'N'"}), 422

        rol = db.session.get(Rol, id)

        if rol is None:
            return jsonify({"message": "Rol no encontrado"}), 404

        try:
            rol.nombre = nombre
            rol.activo = activo
            db.session.commit()

            return jsonify({"message": "Rol actualizado exitosamente"}), 200

        except IntegrityError:
            db.session.rollback()

            return jsonify({"message": "El nombre del rol ya existe"}), 409

    @staticmethod
    def destroy(id: int) -> tuple[Response, int]:
        rol = db.session.get(Rol, id)

        if rol is None:
            return jsonify({"message": "Rol no encontrado"}), 404

        rol.activo = 'N'
        db.session.commit()

        return jsonify({"message": "Rol desactivado exitosamente"}), 200
