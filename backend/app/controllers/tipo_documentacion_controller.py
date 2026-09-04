from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError

from app.controllers import Controller
from app.models import db
from app.models.tipo_documentacion import TipoDocumentacion


class TipoDocumentacionController(Controller):
    @staticmethod
    def get_all() -> tuple[Response, int]:
        tipos_documentacion = db.session.execute(
            db.select(TipoDocumentacion).order_by(db.desc(TipoDocumentacion.id))
        ).scalars().all()

        if tipos_documentacion:
            return jsonify([tipo_documentacion.to_dict() for tipo_documentacion in tipos_documentacion]), 200

        return jsonify({"message": "No se encontraron tipos de documentación"}), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        tipo_documentacion = db.session.get(TipoDocumentacion, id)

        if tipo_documentacion:
            return jsonify(tipo_documentacion.to_dict()), 200

        return jsonify({"message": "Tipo de documentación no encontrado"}), 404

    @staticmethod
    def create(request: dict) -> tuple[Response, int]:
        nombre: str | None = request.get("nombre")
        obligatorio: bool | None = request.get("obligatorio")

        if nombre is None:
            return jsonify({"message": "El nombre es requerido"}), 422

        if obligatorio is None:
            return jsonify({"message": "Debe especificar si el tipo de documentación es obligatorio"}), 422

        try:
            tipo_documentacion = TipoDocumentacion(
                nombre=nombre,
                obligatorio=obligatorio
            )

            db.session.add(tipo_documentacion)
            db.session.commit()

            return jsonify({"message": "Tipo de documentación creado exitosamente"}), 201

        except IntegrityError:
            db.session.rollback()

            return jsonify({"message": "El tipo de documentación ya existe"}), 409

    @staticmethod
    def update(request: dict, id: int) -> tuple[Response, int]:
        nombre: str | None = request.get("nombre")
        obligatorio: bool | None = request.get("obligatorio")
        activo: str | None = request.get("activo")

        if nombre is None:
            return jsonify({"message": "El nombre es requerido"}), 422

        if obligatorio is None:
            return jsonify({"message": "Debe especificar si el tipo de documentación es obligatorio"}), 422

        if activo is None:
            return jsonify({"message": "El estado activo es requerido"}), 422

        if activo not in ["S", "N"]:
            return jsonify({"message": "El estado activo debe ser S o N"}), 422

        tipo_documentacion = db.session.get(TipoDocumentacion, id)

        if tipo_documentacion:
            try:
                tipo_documentacion.nombre = nombre
                tipo_documentacion.obligatorio = obligatorio
                tipo_documentacion.activo = activo
                db.session.commit()
                return jsonify({"message": "Tipo de documentación actualizado exitosamente"}), 200

            except IntegrityError:
                db.session.rollback()

                return jsonify({
                    "message": "El nombre del tipo de documentación ya existe"
                }), 409

        return jsonify({"message": "Tipo de documentación no encontrado"}), 404

    @staticmethod
    def destroy(id: int) -> tuple[Response, int]:
        tipo_documentacion = db.session.get(TipoDocumentacion, id)

        if not tipo_documentacion:
            return jsonify({"message": "Tipo de documentación no encontrado"}), 404

        tipo_documentacion.activo = "N"
        db.session.commit()

        return jsonify({"message": "Tipo de documentación desactivado exitosamente"}), 200
