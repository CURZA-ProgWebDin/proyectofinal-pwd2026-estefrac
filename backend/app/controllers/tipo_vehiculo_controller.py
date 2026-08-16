from app.controllers import Controller
from app.models import db
from app.models.tipo_vehiculo import TipoVehiculo
from sqlalchemy.exc import IntegrityError
from flask import Response, jsonify

class TipoVehiculoController(Controller):
    @staticmethod
    def get_all() -> tuple[Response, int]:
        tipos_vehiculos = db.session.execute(
            db.select(TipoVehiculo).order_by(db.desc(TipoVehiculo.id))
        ).scalars().all()

        if tipos_vehiculos:
            return jsonify([
                tipo_vehiculo.to_dict()
                for tipo_vehiculo in tipos_vehiculos
            ]), 200

        return jsonify({"message": "Tipos de vehículos no encontrados"}), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        tipo_vehiculo = db.session.get(TipoVehiculo, id)

        if tipo_vehiculo:
            return jsonify(tipo_vehiculo.to_dict()), 200

        return jsonify({"message": "Tipo de vehículo no encontrado"}), 404

    @staticmethod
    def create(request: dict) -> tuple[Response, int]:
        nombre: str | None = request.get("nombre")
        unidad_uso: str | None = request.get("unidad_uso")

        if nombre is None:
            return jsonify({"message": "El nombre es requerido"}), 422

        if unidad_uso is None:
            return jsonify({"message": "La unidad de uso es requerida"}), 422

        if unidad_uso not in ["kilometros", "horas"]:
            return jsonify({"message": "La unidad de uso debe ser kilometros u horas"}), 422

        try:
            tipo_vehiculo = TipoVehiculo(nombre=nombre, unidad_uso=unidad_uso)
            db.session.add(tipo_vehiculo)
            db.session.commit()
            return jsonify({
                "message": "Tipo de vehículo creado exitosamente"
            }), 201

        except IntegrityError:
            db.session.rollback()

            return jsonify({
                "message": "El nombre del tipo de vehículo ya existe"
            }), 409

    @staticmethod
    def update(request: dict, id: int) -> tuple[Response, int]:
        nombre: str | None = request.get("nombre")
        unidad_uso: str | None = request.get("unidad_uso")
        activo: str | None = request.get("activo")

        if nombre is None:
            return jsonify({"message": "El nombre es requerido"}), 422

        if unidad_uso is None:
            return jsonify({"message": "La unidad de uso es requerida"}), 422

        if unidad_uso not in ["kilometros", "horas"]:
            return jsonify({"message": "La unidad de uso debe ser kilometros u horas"}), 422

        if activo is None:
            return jsonify({"message": "El estado activo es requerido"}), 422

        if activo not in ["S", "N"]:
            return jsonify({"message": "El estado activo debe ser S o N"}), 422

        tipo_vehiculo = db.session.get(TipoVehiculo, id)

        if tipo_vehiculo:
            try:
                tipo_vehiculo.nombre = nombre
                tipo_vehiculo.unidad_uso = unidad_uso
                tipo_vehiculo.activo = activo
                db.session.commit()
                return jsonify({
                    "message": "Tipo de vehículo actualizado exitosamente"
                }), 200

            except IntegrityError:
                db.session.rollback()

                return jsonify({
                    "message": "El nombre del tipo de vehículo ya existe"
                }), 409

        return jsonify({"message": "Tipo de vehículo no encontrado"}), 404

    @staticmethod
    def destroy(id: int) -> tuple[Response, int]:
        """Desactiva un tipo de vehículo sin eliminarlo físicamente."""

        tipo_vehiculo = db.session.get(TipoVehiculo, id)

        if not tipo_vehiculo:
            return jsonify({"message": "Tipo de vehículo no encontrado"}), 404

        tipo_vehiculo.activo = "N"
        db.session.commit()

        return jsonify({"message": "Tipo de vehículo desactivado exitosamente"}), 200
