from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from zoneinfo import ZoneInfo

from flask import Response, current_app, jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import IntegrityError

from app.models import db
from app.models.mantenimiento import Mantenimiento
from app.models.vehiculo import Vehiculo


class MantenimientoController:
    @staticmethod
    def get_all() -> tuple[Response, int]:
        mantenimientos = (
            db.session.execute(
                db.select(Mantenimiento).order_by(db.desc(Mantenimiento.id))
            )
            .scalars()
            .all()
        )

        if mantenimientos:
            return jsonify(
                [mantenimiento.to_dict() for mantenimiento in mantenimientos]
            ), 200

        return jsonify({"message": "No se encontraron mantenimientos."}), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        mantenimiento = db.session.get(Mantenimiento, id)

        if mantenimiento:
            return jsonify(mantenimiento.to_dict(incluye_relaciones=True)), 200

        return jsonify({"message": "Mantenimiento no encontrado."}), 404

    @staticmethod
    def create(request: dict) -> tuple[Response, int]:
        vehiculo_id: int | None = request.get("vehiculo_id")
        tipo: str | None = request.get("tipo")
        descripcion: str | None = request.get("descripcion")
        fecha_programada_texto = request.get("fecha_programada")
        uso_registrado: int | None = request.get("uso_registrado")
        costo_valor = request.get("costo")
        bloquea_uso = request.get("bloquea_uso", False)
        usuario_id = int(get_jwt_identity())

        if vehiculo_id is None:
            return jsonify({"message": "El vehículo es requerido."}), 422

        if tipo is None:
            return jsonify({"message": "El tipo de mantenimiento es requerido."}), 422

        vehiculo = db.session.get(Vehiculo, vehiculo_id)

        if vehiculo is None or vehiculo.activo != "S":
            return jsonify({"message": "El vehículo no existe o no está activo."}), 422

        fecha_programada: date | None = None

        if fecha_programada_texto is not None:
            try:
                fecha_programada = date.fromisoformat(fecha_programada_texto)
            except (TypeError, ValueError):
                return jsonify(
                    {"message": "La fecha debe tener formato YYYY-MM-DD."}
                ), 422

        if uso_registrado is not None and (
            isinstance(uso_registrado, bool)
            or not isinstance(uso_registrado, int)
            or uso_registrado < 0
        ):
            return jsonify(
                {"message": "El uso registrado debe ser un entero no negativo."}
            ), 422

        costo: Decimal | None = None

        if costo_valor is not None:
            try:
                costo = Decimal(str(costo_valor))
            except (InvalidOperation, ValueError):
                return jsonify(
                    {"message": "El costo debe ser un número válido no negativo."}
                ), 422

            if not costo.is_finite() or costo < 0:
                return jsonify(
                    {"message": "El costo debe ser un número válido no negativo."}
                ), 422

        if not isinstance(bloquea_uso, bool):
            return jsonify({"message": "El bloqueo de uso debe ser booleano."}), 422

        try:
            mantenimiento = Mantenimiento(
                vehiculo_id=vehiculo_id,
                usuario_id=usuario_id,
                tipo=tipo,
                descripcion=descripcion,
                fecha_programada=fecha_programada,
                uso_registrado=uso_registrado,
                costo=costo,
                bloquea_uso=bloquea_uso,
            )

            db.session.add(mantenimiento)
            db.session.commit()

            return jsonify({"message": "Mantenimiento creado exitosamente."}), 201

        except IntegrityError:
            db.session.rollback()

            return jsonify(
                {
                    "message": (
                        "No se pudo crear el mantenimiento "
                        "debido a un conflicto con los datos."
                    )
                }
            ), 409

    @staticmethod
    def update(request: dict, id: int) -> tuple[Response, int]:
        tipo: str | None = request.get("tipo")
        descripcion: str | None = request.get("descripcion")
        fecha_programada_texto = request.get("fecha_programada")
        uso_registrado: int | None = request.get("uso_registrado")
        costo_valor = request.get("costo")
        bloquea_uso = request.get("bloquea_uso")

        if tipo is None:
            return jsonify({"message": "El tipo de mantenimiento es requerido."}), 422

        if "bloquea_uso" not in request:
            return jsonify({"message": "El bloqueo de uso es requerido."}), 422

        mantenimiento = db.session.get(Mantenimiento, id)

        if mantenimiento is None:
            return jsonify({"message": "Mantenimiento no encontrado."}), 404

        if mantenimiento.estado != "pendiente":
            return jsonify(
                {"message": "Solo se puede actualizar un mantenimiento pendiente."}
            ), 409

        fecha_programada: date | None = None

        if fecha_programada_texto is not None:
            try:
                fecha_programada = date.fromisoformat(fecha_programada_texto)
            except (TypeError, ValueError):
                return jsonify(
                    {"message": "La fecha debe tener formato YYYY-MM-DD."}
                ), 422

        if uso_registrado is not None and (
            isinstance(uso_registrado, bool)
            or not isinstance(uso_registrado, int)
            or uso_registrado < 0
        ):
            return jsonify(
                {"message": "El uso registrado debe ser un entero no negativo."}
            ), 422

        costo: Decimal | None = None

        if costo_valor is not None:
            try:
                costo = Decimal(str(costo_valor))
            except (InvalidOperation, ValueError):
                return jsonify(
                    {"message": "El costo debe ser un número válido no negativo."}
                ), 422

            if not costo.is_finite() or costo < 0:
                return jsonify(
                    {"message": "El costo debe ser un número válido no negativo."}
                ), 422

        if not isinstance(bloquea_uso, bool):
            return jsonify({"message": "El bloqueo de uso debe ser booleano."}), 422

        usuario_actualizacion_id = int(get_jwt_identity())

        try:
            mantenimiento.tipo = tipo
            mantenimiento.descripcion = descripcion
            mantenimiento.fecha_programada = fecha_programada
            mantenimiento.uso_registrado = uso_registrado
            mantenimiento.costo = costo
            mantenimiento.bloquea_uso = bloquea_uso
            mantenimiento.usuario_actualizacion_id = usuario_actualizacion_id

            db.session.commit()

            return jsonify({"message": "Mantenimiento actualizado exitosamente."}), 200

        except IntegrityError:
            db.session.rollback()

            return jsonify(
                {
                    "message": (
                        "No se pudo actualizar el mantenimiento "
                        "debido a un conflicto con los datos."
                    )
                }
            ), 409

    @staticmethod
    def complete(request: dict, id: int) -> tuple[Response, int]:
        mantenimiento = db.session.get(Mantenimiento, id)

        if mantenimiento is None:
            return jsonify({"message": "Mantenimiento no encontrado."}), 404

        if mantenimiento.estado != "pendiente":
            return jsonify({"message": "El mantenimiento no está pendiente."}), 409

        fecha_realizada_texto = request.get("fecha_realizada")

        if fecha_realizada_texto is None:
            fecha_realizada = datetime.now(
                tz=ZoneInfo(current_app.config["APP_TIMEZONE"])
            ).date()
        else:
            try:
                fecha_realizada = date.fromisoformat(fecha_realizada_texto)
            except (TypeError, ValueError):
                return jsonify(
                    {"message": "La fecha debe tener formato YYYY-MM-DD."}
                ), 422

        uso_registrado = mantenimiento.uso_registrado

        if "uso_registrado" in request:
            uso_registrado = request.get("uso_registrado")

            if uso_registrado is not None and (
                isinstance(uso_registrado, bool)
                or not isinstance(uso_registrado, int)
                or uso_registrado < 0
            ):
                return jsonify(
                    {"message": "El uso registrado debe ser un entero no negativo."}
                ), 422

        costo = mantenimiento.costo

        if "costo" in request:
            costo_valor = request.get("costo")

            if costo_valor is None:
                costo = None
            else:
                try:
                    costo = Decimal(str(costo_valor))
                except (InvalidOperation, ValueError):
                    return jsonify(
                        {
                            "message": (
                                "El costo debe ser un número válido no negativo."
                            )
                        }
                    ), 422

                if not costo.is_finite() or costo < 0:
                    return jsonify(
                        {
                            "message": (
                                "El costo debe ser un número válido no negativo."
                            )
                        }
                    ), 422

        usuario_actualizacion_id = int(get_jwt_identity())

        try:
            mantenimiento.fecha_realizada = fecha_realizada
            mantenimiento.uso_registrado = uso_registrado
            mantenimiento.costo = costo
            mantenimiento.estado = "realizado"
            mantenimiento.usuario_actualizacion_id = usuario_actualizacion_id

            db.session.commit()

            return jsonify({"message": "Mantenimiento realizado exitosamente."}), 200

        except IntegrityError:
            db.session.rollback()

            return jsonify(
                {
                    "message": (
                        "No se pudo realizar el mantenimiento "
                        "debido a un conflicto con los datos."
                    )
                }
            ), 409

    @staticmethod
    def cancel(id: int) -> tuple[Response, int]:
        mantenimiento = db.session.get(Mantenimiento, id)

        if mantenimiento is None:
            return jsonify({"message": "Mantenimiento no encontrado."}), 404

        if mantenimiento.estado != "pendiente":
            return jsonify({"message": "El mantenimiento no está pendiente."}), 409

        usuario_actualizacion_id = int(get_jwt_identity())

        try:
            mantenimiento.estado = "cancelado"
            mantenimiento.usuario_actualizacion_id = usuario_actualizacion_id

            db.session.commit()

            return jsonify({"message": "Mantenimiento cancelado exitosamente."}), 200

        except IntegrityError:
            db.session.rollback()

            return jsonify(
                {
                    "message": (
                        "No se pudo cancelar el mantenimiento "
                        "debido a un conflicto con los datos."
                    )
                }
            ), 409
