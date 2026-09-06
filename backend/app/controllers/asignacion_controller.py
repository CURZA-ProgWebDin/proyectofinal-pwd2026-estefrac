from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Response, current_app, jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import IntegrityError

from app.models import db
from app.models.asignacion import Asignacion
from app.models.conductor import Conductor
from app.models.vehiculo import Vehiculo


class AsignacionController:
    @staticmethod
    def get_all() -> tuple[Response, int]:
        asignaciones = (
            db.session.execute(db.select(Asignacion).order_by(db.desc(Asignacion.id)))
            .scalars()
            .all()
        )

        if asignaciones:
            return jsonify([asignacion.to_dict() for asignacion in asignaciones]), 200

        return jsonify({"message": "No se encontraron asignaciones."}), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        asignacion = db.session.get(Asignacion, id)

        if asignacion:
            return jsonify(asignacion.to_dict(incluye_relaciones=True)), 200

        return jsonify({"message": "Asignación no encontrada."}), 404

    @staticmethod
    def create(request: dict) -> tuple[Response, int]:
        vehiculo_id: int | None = request.get("vehiculo_id")
        conductor_id: int | None = request.get("conductor_id")
        destino: str | None = request.get("destino")
        motivo: str | None = request.get("motivo")
        usuario_id: int = int(get_jwt_identity())

        if vehiculo_id is None:
            return jsonify({"message": "El vehículo es requerido."}), 422

        if conductor_id is None:
            return jsonify({"message": "El conductor es requerido."}), 422

        vehiculo = db.session.get(Vehiculo, vehiculo_id)

        if vehiculo is None or vehiculo.activo != "S":
            return jsonify({"message": "El vehículo no existe o no está activo."}), 422

        conductor = db.session.get(Conductor, conductor_id)

        if conductor is None or conductor.activo != "S":
            return jsonify({"message": "El conductor no existe o no está activo."}), 422

        hoy = datetime.now(tz=ZoneInfo(current_app.config["APP_TIMEZONE"])).date()

        if conductor.licencia_vencimiento < hoy:
            return jsonify({"message": "La licencia del conductor está vencida."}), 409

        if vehiculo.estado != "disponible":
            return jsonify({"message": "El vehículo no está disponible."}), 409

        asignacion_vehiculo = db.session.execute(
            db.select(Asignacion).filter_by(
                vehiculo_id=vehiculo_id,
                estado="abierta",
            )
        ).scalar_one_or_none()

        if asignacion_vehiculo:
            return jsonify(
                {"message": "El vehículo ya tiene una asignación abierta."}
            ), 409

        asignacion_conductor = db.session.execute(
            db.select(Asignacion).filter_by(conductor_id=conductor_id, estado="abierta")
        ).scalar_one_or_none()

        if asignacion_conductor:
            return jsonify({"message": "El conductor no está disponible."}), 409

        try:
            asignacion = Asignacion(
                vehiculo_id=vehiculo_id,
                conductor_id=conductor_id,
                usuario_id=usuario_id,
                uso_salida=vehiculo.uso_actual,
                destino=destino,
                motivo=motivo,
            )

            vehiculo.estado = "en_uso"

            db.session.add(asignacion)
            db.session.commit()

            return jsonify({"message": "Asignación creada exitosamente."}), 201

        except IntegrityError:
            db.session.rollback()

            return jsonify(
                {"message": "El vehículo o conductor ya tiene una asignación abierta."}
            ), 409
