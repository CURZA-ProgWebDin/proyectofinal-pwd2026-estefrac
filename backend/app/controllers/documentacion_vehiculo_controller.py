from app.controllers import Controller
from app.models import db
from app.models.vehiculo import Vehiculo
from app.models.tipo_documentacion import TipoDocumentacion
from app.models.documentacion_vehiculo import DocumentacionVehiculo
from flask import Response, jsonify
from datetime import date
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity

class DocumentacionVehiculoController(Controller):
    @staticmethod
    def get_all() -> tuple[Response, int]:
        documentaciones = db.session.execute(
            db.select(DocumentacionVehiculo).order_by(db.desc(DocumentacionVehiculo.id))
        ).scalars().all()

        if documentaciones:
            return jsonify([
                documentacion.to_dict()
                for documentacion in documentaciones
            ]), 200

        return jsonify({
            "message": "No se encontró documentación vehicular"
        }), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        documentacion = db.session.get(DocumentacionVehiculo, id)

        if documentacion:
            return jsonify(documentacion.to_dict(incluye_tipo_documentacion=True)), 200

        return jsonify({
            "message": "Documentación vehicular no encontrada"
        }), 404

    @staticmethod
    def create(request: dict) -> tuple[Response, int]:
        vehiculo_id: int | None = request.get("vehiculo_id")
        tipo_documentacion_id: int | None = request.get("tipo_documentacion_id")
        numero: str | None = request.get("numero")
        fecha_emision: str | None = request.get("fecha_emision")
        fecha_vencimiento: str | None = request.get("fecha_vencimiento")
        usuario_id: int = int(get_jwt_identity())

        if vehiculo_id is None:
            return jsonify({
                "message": "El vehículo es requerido"
            }), 422

        if tipo_documentacion_id is None:
            return jsonify({
                "message": "El tipo de documentación es requerido"
            }), 422

        if fecha_vencimiento is None:
            return jsonify({
                "message": "La fecha de vencimiento es requerida"
            }), 422

        vehiculo = db.session.get(Vehiculo, vehiculo_id)

        if vehiculo is None or vehiculo.activo != "S":
            return jsonify({
                "message": "El vehículo no existe o no está activo"
            }), 422

        tipo_documentacion = db.session.get(
            TipoDocumentacion,
            tipo_documentacion_id
        )

        if (
            tipo_documentacion is None
            or tipo_documentacion.activo != "S"
        ):
            return jsonify({
                "message": (
                    "El tipo de documentación no existe "
                    "o no está activo"
                )
            }), 422

        try:
            fecha_emision_convertida: date | None = (
                date.fromisoformat(fecha_emision)
                if fecha_emision
                else None
            )
            fecha_vencimiento_convertida: date = date.fromisoformat(
                fecha_vencimiento
            )

        except (TypeError, ValueError):
            return jsonify({
                "message": "Las fechas deben tener formato YYYY-MM-DD"
            }), 422

        if (
            fecha_emision_convertida is not None
            and fecha_emision_convertida > fecha_vencimiento_convertida
        ):
            return jsonify({
                "message": (
                    "La fecha de emisión no puede ser posterior "
                    "a la fecha de vencimiento"
                )
            }), 422

        try:
            documentacion = DocumentacionVehiculo(
                vehiculo_id=vehiculo_id,
                tipo_documentacion_id=tipo_documentacion_id,
                usuario_id=usuario_id,
                numero=numero,
                fecha_emision=fecha_emision_convertida,
                fecha_vencimiento=fecha_vencimiento_convertida
            )

            db.session.add(documentacion)
            db.session.commit()

            return jsonify({
                "message": "Documentación vehicular creada exitosamente"
            }), 201

        except IntegrityError:
            db.session.rollback()

            return jsonify({
                "message": (
                    "No se pudo crear la documentación vehicular "
                    "debido a un conflicto con los datos"
                )
            }), 409

    @staticmethod
    def update(request: dict, id: int) -> tuple[Response, int]:
        vehiculo_id: int | None = request.get("vehiculo_id")
        tipo_documentacion_id: int | None = request.get(
            "tipo_documentacion_id"
        )
        numero: str | None = request.get("numero")
        fecha_emision: str | None = request.get("fecha_emision")
        fecha_vencimiento: str | None = request.get("fecha_vencimiento")
        activo: str | None = request.get("activo")
        usuario_actualizacion_id: int = int(get_jwt_identity())

        if vehiculo_id is None:
            return jsonify({
                "message": "El vehículo es requerido"
            }), 422

        if tipo_documentacion_id is None:
            return jsonify({
                "message": "El tipo de documentación es requerido"
            }), 422

        if fecha_vencimiento is None:
            return jsonify({
                "message": "La fecha de vencimiento es requerida"
            }), 422

        if activo is None:
            return jsonify({
                "message": "El estado activo es requerido"
            }), 422

        if activo not in ["S", "N"]:
            return jsonify({
                "message": "El estado activo debe ser S o N"
            }), 422

        documentacion = db.session.get(DocumentacionVehiculo, id)

        if documentacion is None:
            return jsonify({
                "message": "Documentación vehicular no encontrada"
            }), 404

        vehiculo = db.session.get(Vehiculo, vehiculo_id)

        if vehiculo is None or vehiculo.activo != "S":
            return jsonify({
                "message": "El vehículo no existe o no está activo"
            }), 422

        tipo_documentacion = db.session.get(
            TipoDocumentacion,
            tipo_documentacion_id
        )

        if (
            tipo_documentacion is None
            or tipo_documentacion.activo != "S"
        ):
            return jsonify({
                "message": (
                    "El tipo de documentación no existe "
                    "o no está activo"
                )
            }), 422

        try:
            fecha_emision_convertida: date | None = (
                date.fromisoformat(fecha_emision)
                if fecha_emision
                else None
            )
            fecha_vencimiento_convertida: date = date.fromisoformat(
                fecha_vencimiento
            )

        except (TypeError, ValueError):
            return jsonify({
                "message": "Las fechas deben tener formato YYYY-MM-DD"
            }), 422

        if (
            fecha_emision_convertida is not None
            and fecha_emision_convertida > fecha_vencimiento_convertida
        ):
            return jsonify({
                "message": (
                    "La fecha de emisión no puede ser posterior "
                    "a la fecha de vencimiento"
                )
            }), 422

        try:
            documentacion.vehiculo_id = vehiculo_id
            documentacion.tipo_documentacion_id = tipo_documentacion_id
            documentacion.numero = numero
            documentacion.fecha_emision = fecha_emision_convertida
            documentacion.fecha_vencimiento = fecha_vencimiento_convertida
            documentacion.usuario_actualizacion_id = usuario_actualizacion_id
            documentacion.activo = activo

            db.session.commit()

            return jsonify({
                "message": (
                    "Documentación vehicular actualizada exitosamente"
                )
            }), 200

        except IntegrityError:
            db.session.rollback()

            return jsonify({
                "message": (
                    "No se pudo actualizar la documentación vehicular "
                    "debido a un conflicto con los datos"
                )
            }), 409

    @staticmethod
    def destroy(id: int) -> tuple[Response, int]:
        documentacion = db.session.get(DocumentacionVehiculo, id)

        if documentacion is None:
            return jsonify({
                "message": "Documentación vehicular no encontrada"
            }), 404

        documentacion.usuario_actualizacion_id = int(
            get_jwt_identity()
        )
        documentacion.activo = "N"

        db.session.commit()

        return jsonify({
            "message": "Documentación vehicular desactivada exitosamente"
        }), 200
