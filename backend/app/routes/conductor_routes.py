from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.conductor_controller import ConductorController
from app.decorators.rol_access import rol_access


conductor_bp = Blueprint(
    "conductor",
    __name__,
    url_prefix="/conductores"
)


@conductor_bp.route("/", methods=["GET"])
@jwt_required()
@rol_access(["admin", "operador"])
def get_all():
    return ConductorController.get_all()


@conductor_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
@rol_access(["admin", "operador"])
def show(id: int):
    return ConductorController.show(id)


@conductor_bp.route("/", methods=["POST"])
@jwt_required()
@rol_access(["admin"])
def create():
    return ConductorController.create(request.get_json())


@conductor_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@rol_access(["admin"])
def update(id: int):
    return ConductorController.update(
        request=request.get_json(),
        id=id
    )


@conductor_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@rol_access(["admin"])
def destroy(id: int):
    return ConductorController.destroy(id)
