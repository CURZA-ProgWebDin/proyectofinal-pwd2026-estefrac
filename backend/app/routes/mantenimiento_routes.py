from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.mantenimiento_controller import MantenimientoController
from app.decorators.rol_access import rol_access

mantenimiento_bp = Blueprint(
    "mantenimiento",
    __name__,
    url_prefix="/mantenimientos",
)


@mantenimiento_bp.route("/", methods=["GET"])
@jwt_required()
@rol_access(["admin", "operador"])
def get_all():
    return MantenimientoController.get_all()


@mantenimiento_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
@rol_access(["admin", "operador"])
def show(id: int):
    return MantenimientoController.show(id)


@mantenimiento_bp.route("/", methods=["POST"])
@jwt_required()
@rol_access(["admin"])
def create():
    return MantenimientoController.create(request.get_json())


@mantenimiento_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@rol_access(["admin"])
def update(id: int):
    return MantenimientoController.update(
        request=request.get_json(),
        id=id,
    )


@mantenimiento_bp.route("/<int:id>/realizar", methods=["POST"])
@jwt_required()
@rol_access(["admin"])
def complete(id: int):
    return MantenimientoController.complete(
        request=request.get_json(),
        id=id,
    )


@mantenimiento_bp.route("/<int:id>/cancelar", methods=["POST"])
@jwt_required()
@rol_access(["admin"])
def cancel(id: int):
    return MantenimientoController.cancel(id)
