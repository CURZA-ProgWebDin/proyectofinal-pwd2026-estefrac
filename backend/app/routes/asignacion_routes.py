from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.asignacion_controller import AsignacionController
from app.decorators.rol_access import rol_access

asignacion_bp = Blueprint(
    "asignacion",
    __name__,
    url_prefix="/asignaciones",
)


@asignacion_bp.route("/", methods=["GET"])
@jwt_required()
@rol_access(["admin", "operador"])
def get_all():
    return AsignacionController.get_all()


@asignacion_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
@rol_access(["admin", "operador"])
def show(id: int):
    return AsignacionController.show(id)


@asignacion_bp.route("/", methods=["POST"])
@jwt_required()
@rol_access(["admin", "operador"])
def create():
    return AsignacionController.create(request.get_json())


@asignacion_bp.route("/<int:id>/cerrar", methods=["POST"])
@jwt_required()
@rol_access(["admin", "operador"])
def close(id: int):
    return AsignacionController.close(
        request=request.get_json(),
        id=id,
    )


@asignacion_bp.route("/<int:id>/cancelar", methods=["POST"])
@jwt_required()
@rol_access(["admin", "operador"])
def cancel(id: int):
    return AsignacionController.cancel(id)
