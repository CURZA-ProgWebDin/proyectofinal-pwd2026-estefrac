from app.controllers import Controller
from app.models import db
from app.models.conductor import Conductor
from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError
from datetime import date

class ConductorController(Controller):
    @staticmethod
    def get_all() -> tuple[Response, int]:
        conductores = db.session.execute(
            db.select(Conductor).order_by(db.desc(Conductor.id))
        ).scalars().all()

        if conductores:
            return jsonify([conductor.to_dict() for conductor in conductores]), 200

        return jsonify({"message": "No se encontraron conductores"}), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        conductor = db.session.get(Conductor, id)
        
        if conductor:
            return jsonify(conductor.to_dict()), 200

        return jsonify({"message": "Conductor no encontrado"}), 404

    @staticmethod
    def create(request: dict) -> tuple[Response, int]:
        nombre: str | None = request.get("nombre")
        apellido: str | None = request.get("apellido")
        dni: str | None = request.get("dni")
        telefono: str | None = request.get("telefono")
        licencia_numero: str | None = request.get("licencia_numero")
        licencia_vencimiento_texto: str | None = request.get("licencia_vencimiento")

        if nombre is None:
            return jsonify({"message": "El nombre es requerido"}), 422

        if apellido is None:
            return jsonify({"message": "El apellido es requerido"}), 422

        if dni is None:
            return jsonify({"message": "El DNI es requerido"}), 422

        if telefono is None:
            return jsonify({"message": "El teléfono es requerido"}), 422

        if licencia_numero is None:
            return jsonify({"message": "El número de licencia es requerido"}), 422

        if licencia_vencimiento_texto is None:
            return jsonify({"message": "El vencimiento de la licencia es requerido"}), 422

        try:
            licencia_vencimiento = date.fromisoformat(licencia_vencimiento_texto)
        except (TypeError, ValueError):
            return jsonify({"message": "El vencimiento debe tener formato YYYY-MM-DD"}), 422

        try:
            conductor = Conductor(
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                telefono=telefono,
                licencia_numero=licencia_numero,
                licencia_vencimiento=licencia_vencimiento
            )

            db.session.add(conductor)
            db.session.commit()

            return jsonify({"message": "Conductor creado exitosamente"}), 201

        except IntegrityError:
            db.session.rollback()

        return jsonify({"message": "El DNI o número de licencia ya existe"}), 409

    @staticmethod
    def update(request: dict, id: int) -> tuple[Response, int]:
        nombre: str | None = request.get("nombre")
        apellido: str | None = request.get("apellido")
        dni: str | None = request.get("dni")
        telefono: str | None = request.get("telefono")
        licencia_numero: str | None = request.get("licencia_numero")
        licencia_vencimiento_texto: str | None = request.get("licencia_vencimiento")
        activo: str | None = request.get("activo")

        if nombre is None:
            return jsonify({"message": "El nombre es requerido"}), 422

        if apellido is None:
            return jsonify({"message": "El apellido es requerido"}), 422

        if dni is None:
            return jsonify({"message": "El DNI es requerido"}), 422

        if telefono is None:
            return jsonify({"message": "El teléfono es requerido"}), 422

        if licencia_numero is None:
            return jsonify({"message": "El número de licencia es requerido"}), 422

        if licencia_vencimiento_texto is None:
            return jsonify({"message": "El vencimiento de la licencia es requerido"}), 422

        if activo is None:
            return jsonify({"message": "El estado activo es requerido"}), 422

        if activo not in ["S", "N"]:
            return jsonify({"message": "El estado activo debe ser S o N"}), 422

        try:
            licencia_vencimiento = date.fromisoformat(licencia_vencimiento_texto)
        except (TypeError, ValueError):
            return jsonify({"message": "El vencimiento debe tener formato YYYY-MM-DD"}), 422

        conductor = db.session.get(Conductor, id)

        if conductor is None:
            return jsonify({"message": "Conductor no encontrado"}), 404

        try:
            conductor.nombre = nombre
            conductor.apellido = apellido
            conductor.dni = dni
            conductor.telefono = telefono
            conductor.licencia_numero = licencia_numero
            conductor.licencia_vencimiento = licencia_vencimiento
            conductor.activo = activo

            db.session.commit()

            return jsonify({"message": "Conductor actualizado exitosamente"}), 200

        except IntegrityError:
            db.session.rollback()

            return jsonify({"message": "El DNI o número de licencia ya existe"}), 409

    @staticmethod
    def destroy(id: int) -> tuple[Response, int]:
        conductor = db.session.get(Conductor, id)

        if conductor is None:
            return jsonify({"message": "Conductor no encontrado"}), 404

        conductor.activo = "N"
        db.session.commit()

        return jsonify({"message": "Conductor desactivado exitosamente"}), 200
