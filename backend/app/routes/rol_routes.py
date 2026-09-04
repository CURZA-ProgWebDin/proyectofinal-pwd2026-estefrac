from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.rol_controller import RolController
from app.decorators.rol_access import rol_access

rol_bp = Blueprint('rol', __name__, url_prefix='/roles')

@rol_bp.route('/', methods=['GET'])
@jwt_required()
@rol_access(["admin"])
def get_all():
    return RolController.get_all()

@rol_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@rol_access(["admin"])
def show(id: int):
    return RolController.show(id)

@rol_bp.route('/', methods=['POST'])
@jwt_required()
@rol_access(["admin"])
def create():
    return RolController.create(request.get_json())

@rol_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@rol_access(["admin"])
def update(id: int):
    return RolController.update(request=request.get_json(), id=id)

@rol_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@rol_access(["admin"])
def destroy(id: int):
    return RolController.destroy(id)
