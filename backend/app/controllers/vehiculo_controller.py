from app.controllers import Controller
from app.models import db
from app.models.vehiculo import Vehiculo
from app.models.tipo_vehiculo import TipoVehiculo
from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError

class VehiculoController(Controller):
    @staticmethod
    def get_all() -> tuple[Response, int]:
        vehiculos = db.session.execute(
            db.select(Vehiculo).order_by(db.desc(Vehiculo.id))
        ).scalars().all()

        if vehiculos:
            return jsonify([vehiculo.to_dict() for vehiculo in vehiculos]), 200

        return jsonify({"message": "No se encontraron vehículos."}), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        vehiculo = db.session.get(Vehiculo, id)

        if vehiculo:
            return jsonify(vehiculo.to_dict()), 200

        return jsonify({"message": "Vehículo no encontrado."}), 404

    @staticmethod
    def create(request: dict) -> tuple[Response, int]:
        patente: str | None = request.get("patente")
        marca: str | None = request.get("marca")
        modelo: str | None = request.get("modelo")
        anio: int | None = request.get("anio")
        tipo_vehiculo_id: int | None = request.get("tipo_vehiculo_id")
        uso_actual: int | None = request.get("uso_actual", 0)

        error: str | None = None

        if patente is None:
            error = "La patente es requerida."

        if marca is None:
            error = "La marca es requerida"

        if modelo is None:
            error = "El modelo es requerido."

        if tipo_vehiculo_id is None:
            error = "El tipo de vehículo es requerido."

        if uso_actual is None:
            error = "El uso actual es requerido."

        if uso_actual is not None and uso_actual < 0:
            error = "El uso actual no puede ser negativo."

        if anio is None:
            error = "El año es requerido."

        if (
            error is None
            and patente is not None
            and marca is not None
            and modelo is not None
            and anio is not None
            and tipo_vehiculo_id is not None
            and uso_actual is not None
        ):
            tipo_vehiculo = db.session.get(TipoVehiculo, tipo_vehiculo_id)

            if tipo_vehiculo is None or tipo_vehiculo.activo != "S":
                return jsonify({
                    "message": "El tipo de vehículo no existe o no está activo."
                }), 422

            try:
                vehiculo = Vehiculo(
                    patente=patente,
                    marca=marca,
                    modelo=modelo,
                    anio=anio,
                    tipo_vehiculo_id=tipo_vehiculo_id,
                    uso_actual=uso_actual
                )

                db.session.add(vehiculo)
                db.session.commit()

                return jsonify({
                    "message": "Vehículo creado exitosamente.",
                }), 201

            except IntegrityError:
                db.session.rollback()

                return jsonify({
                    "message": "La patente del vehículo ya existe.",
                }), 409

        return jsonify({"message": error}), 422


    @staticmethod
    def update(request: dict, id: int) -> tuple[Response, int]:
        patente: str | None = request.get("patente")
        marca: str | None = request.get("marca")
        modelo: str | None = request.get("modelo")
        anio: int | None = request.get("anio")
        tipo_vehiculo_id: int | None = request.get("tipo_vehiculo_id")
        uso_actual: int | None = request.get("uso_actual")
        estado: str | None = request.get("estado")
        activo: str | None = request.get("activo")

        error: str | None = None

        if patente is None:
            error = "La patente es requerida."

        if marca is None:
            error = "La marca es requerida."

        if modelo is None:
            error = "El modelo es requerido."

        if anio is None:
            error = "El año es requerido."

        if tipo_vehiculo_id is None:
            error = "El tipo de vehículo es requerido."

        if uso_actual is None:
            error = "El uso actual es requerido."

        if uso_actual is not None and uso_actual < 0:
            error = "El uso actual no puede ser negativo."

        if estado is None:
            error = "El estado es requerido."

        if estado is not None and estado not in [
            "disponible",
            "en_uso",
            "mantenimiento",
            "fuera_de_servicio"
        ]:
            error = "El estado del vehículo no es válido."

        if activo is None:
            error = "El estado activo es requerido."

        if activo is not None and activo not in ["S", "N"]:
            error = "El estado activo debe ser S o N."

        if (
            error is None
            and patente is not None
            and marca is not None
            and modelo is not None
            and anio is not None
            and tipo_vehiculo_id is not None
            and uso_actual is not None
            and estado is not None
            and activo is not None
        ):
            vehiculo = db.session.get(Vehiculo, id)

            if vehiculo is None:
                return jsonify({"message": "Vehículo no encontrado."}), 404

            tipo_vehiculo = db.session.get(TipoVehiculo, tipo_vehiculo_id)

            if tipo_vehiculo is None or tipo_vehiculo.activo != "S":
                return jsonify({
                    "message": "El tipo de vehículo no existe o no está activo."
                }), 422

            try:
                vehiculo.patente = patente
                vehiculo.marca = marca
                vehiculo.modelo = modelo
                vehiculo.anio = anio
                vehiculo.tipo_vehiculo_id = tipo_vehiculo_id
                vehiculo.uso_actual = uso_actual
                vehiculo.estado = estado
                vehiculo.activo = activo

                db.session.commit()

                return jsonify({
                    "message": "Vehículo actualizado exitosamente.",
                }), 200

            except IntegrityError:
                db.session.rollback()

                return jsonify({
                    "message": "La patente del vehículo ya existe.",
                }), 409

        return jsonify({"message": error}), 422

    @staticmethod
    def destroy(id: int) -> tuple[Response, int]:
        vehiculo = db.session.get(Vehiculo, id)

        if vehiculo is None:
            return jsonify({"message": "Vehículo no encontrado."}), 404

        vehiculo.activo = "N"
        db.session.commit()

        return jsonify({"message": "Vehículo desactivado exitosamente."}), 200
