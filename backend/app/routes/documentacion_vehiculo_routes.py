from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.documentacion_vehiculo_controller import (
    DocumentacionVehiculoController
)
from app.decorators.rol_access import rol_access


documentacion_vehiculo_bp = Blueprint(
    "documentacion_vehiculo",
    __name__,
    url_prefix="/documentaciones-vehiculos"
)

@documentacion_vehiculo_bp.route("/", methods=["GET"])
@jwt_required()
@rol_access(["admin", "operador"])
def get_all():
    return DocumentacionVehiculoController.get_all()


@documentacion_vehiculo_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
@rol_access(["admin", "operador"])
def show(id: int):
    return DocumentacionVehiculoController.show(id)

@documentacion_vehiculo_bp.route("/", methods=["POST"])
@jwt_required()
@rol_access(["admin"])
def create():
    return DocumentacionVehiculoController.create(request.get_json())


@documentacion_vehiculo_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@rol_access(["admin"])
def update(id: int):
    return DocumentacionVehiculoController.update(
        request=request.get_json(),
        id=id
    )


@documentacion_vehiculo_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@rol_access(["admin"])
def destroy(id: int):
    return DocumentacionVehiculoController.destroy(id)
