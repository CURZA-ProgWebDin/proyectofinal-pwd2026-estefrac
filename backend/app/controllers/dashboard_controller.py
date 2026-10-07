from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from flask import Response, current_app, jsonify

from app.models import db
from app.models.asignacion import Asignacion
from app.models.conductor import Conductor
from app.models.documentacion_vehiculo import DocumentacionVehiculo
from app.models.mantenimiento import Mantenimiento
from app.models.vehiculo import Vehiculo


class DashboardController:
    @staticmethod
    def get_resumen() -> tuple[Response, int]:
        hoy = datetime.now(tz=ZoneInfo(current_app.config["APP_TIMEZONE"])).date()
        limite = hoy + timedelta(days=30)

        vehiculos_activos = db.session.execute(
            db.select(db.func.count())
            .select_from(Vehiculo)
            .where(Vehiculo.activo == "S")
        ).scalar_one()

        conductores_activos = db.session.execute(
            db.select(db.func.count())
            .select_from(Conductor)
            .where(Conductor.activo == "S")
        ).scalar_one()

        vehiculos_asignados = db.session.execute(
            db.select(db.func.count())
            .select_from(Asignacion)
            .where(Asignacion.estado == "abierta")
        ).scalar_one()

        mantenimientos_programados = db.session.execute(
            db.select(db.func.count())
            .select_from(Mantenimiento)
            .where(
                Mantenimiento.activo == "S",
                Mantenimiento.estado == "pendiente",
                Mantenimiento.fecha_programada >= hoy,  # type: ignore[operator]
                Mantenimiento.fecha_programada <= limite,  # type: ignore[operator]
            )
        ).scalar_one()

        documentos_por_vencer = db.session.execute(
            db.select(db.func.count())
            .select_from(DocumentacionVehiculo)
            .where(
                DocumentacionVehiculo.activo == "S",
                DocumentacionVehiculo.fecha_vencimiento >= hoy,
                DocumentacionVehiculo.fecha_vencimiento <= limite,
            )
        ).scalar_one()

        actividad_reciente = (
            db.session.execute(
                db.select(Asignacion)
                .where(Asignacion.activo == "S", Asignacion.estado != "cancelada")
                .order_by(db.desc(Asignacion.fecha_salida))
                .limit(5)
            )
            .scalars()
            .all()
        )

        actividad_reciente = [
            asignacion.to_dict(incluye_relaciones=True)
            for asignacion in actividad_reciente
        ]

        return jsonify(
            {
                "vehiculos_activos": vehiculos_activos,
                "conductores_activos": conductores_activos,
                "vehiculos_asignados": vehiculos_asignados,
                "mantenimientos_programados": mantenimientos_programados,
                "documentos_por_vencer": documentos_por_vencer,
                "actividad_reciente": actividad_reciente,
            }
        ), 200
