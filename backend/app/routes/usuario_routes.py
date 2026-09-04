from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.usuario_controller import UsuarioController
from app.decorators.rol_access import rol_access

usuario_bp = Blueprint(
    "usuario",
    __name__,
    url_prefix="/usuarios"
)


@usuario_bp.route("/", methods=["GET"])
@jwt_required()
@rol_access(["admin"])
def get_all():
    return UsuarioController.get_all()


@usuario_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
@rol_access(["admin"])
def show(id: int):
    return UsuarioController.show(id)


@usuario_bp.route("/", methods=["POST"])
@jwt_required()
@rol_access(["admin"])
def create():
    return UsuarioController.create(request.get_json())


@usuario_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@rol_access(["admin"])
def update(id: int):
    return UsuarioController.update(
        request=request.get_json(),
        id=id
    )


@usuario_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@rol_access(["admin"])
def destroy(id: int):
    return UsuarioController.destroy(id)
