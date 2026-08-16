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

        if patente is None:
            return jsonify({"message": "La patente es requerida."}), 422

        if marca is None:
            return jsonify({"message": "La marca es requerida"}), 422

        if modelo is None:
            return jsonify({"message": "El modelo es requerido."}), 422

        if anio is None:
            return jsonify({"message": "El año es requerido."}), 422

        if tipo_vehiculo_id is None:
            return jsonify({"message": "El tipo de vehículo es requerido."}), 422

        if uso_actual is None:
            return jsonify({"message": "El uso actual es requerido."}), 422

        if uso_actual < 0:
            return jsonify({"message": "El uso actual no puede ser negativo."}), 422

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

        if patente is None:
            return jsonify({"message": "La patente es requerida."}), 422

        if marca is None:
            return jsonify({"message": "La marca es requerida."}), 422

        if modelo is None:
            return jsonify({"message": "El modelo es requerido."}), 422

        if anio is None:
            return jsonify({"message": "El año es requerido."}), 422

        if tipo_vehiculo_id is None:
            return jsonify({"message": "El tipo de vehículo es requerido."}), 422

        if uso_actual is None:
            return jsonify({"message": "El uso actual es requerido."}), 422

        if uso_actual < 0:
            return jsonify({"message": "El uso actual no puede ser negativo."}), 422

        if estado is None:
            return jsonify({"message": "El estado es requerido."}), 422

        if estado not in [
            "disponible",
            "en_uso",
            "mantenimiento",
            "fuera_de_servicio"
        ]:
            return jsonify({"message": "El estado del vehículo no es válido."}), 422

        if activo is None:
            return jsonify({"message": "El estado activo es requerido."}), 422

        if activo not in ["S", "N"]:
            return jsonify({"message": "El estado activo debe ser S o N."}), 422

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

    @staticmethod
    def destroy(id: int) -> tuple[Response, int]:
        vehiculo = db.session.get(Vehiculo, id)

        if vehiculo is None:
            return jsonify({"message": "Vehículo no encontrado."}), 404

        vehiculo.activo = "N"
        db.session.commit()

        return jsonify({"message": "Vehículo desactivado exitosamente."}), 200
