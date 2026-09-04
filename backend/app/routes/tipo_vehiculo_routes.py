from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.tipo_vehiculo_controller import TipoVehiculoController
from app.decorators.rol_access import rol_access

tipo_vehiculo_bp = Blueprint('tipo_vehiculo', __name__, url_prefix='/tipos-vehiculos')

@tipo_vehiculo_bp.route('/', methods=['GET'])
@jwt_required()
@rol_access(["admin", "operador"])
def get_all():
    return TipoVehiculoController.get_all()

@tipo_vehiculo_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@rol_access(["admin", "operador"])
def show(id: int):
    return TipoVehiculoController.show(id)

@tipo_vehiculo_bp.route('/', methods=['POST'])
@jwt_required()
@rol_access(["admin"])
def create():
    return TipoVehiculoController.create(request.get_json())

@tipo_vehiculo_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@rol_access(["admin"])
def update(id: int):
    return TipoVehiculoController.update(request=request.get_json(), id=id)

@tipo_vehiculo_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@rol_access(["admin"])
def destroy(id: int):
    return TipoVehiculoController.destroy(id)
