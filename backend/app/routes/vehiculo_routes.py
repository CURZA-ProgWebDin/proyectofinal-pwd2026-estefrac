from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.vehiculo_controller import VehiculoController
from app.decorators.rol_access import rol_access

vehiculo_bp = Blueprint(
    "vehiculo",
    __name__,
    url_prefix="/vehiculos"
)


@vehiculo_bp.route("/", methods=["GET"])
@jwt_required()
@rol_access(["admin", "operador"])
def get_all():
    return VehiculoController.get_all()


@vehiculo_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
@rol_access(["admin", "operador"])
def show(id: int):
    return VehiculoController.show(id)


@vehiculo_bp.route("/", methods=["POST"])
@jwt_required()
@rol_access(["admin"])
def create():
    return VehiculoController.create(request.get_json())


@vehiculo_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@rol_access(["admin"])
def update(id: int):
    return VehiculoController.update(request=request.get_json(), id=id)


@vehiculo_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@rol_access(["admin"])
def destroy(id: int):
    return VehiculoController.destroy(id)
