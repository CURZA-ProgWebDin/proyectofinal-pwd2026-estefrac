from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.tipo_documentacion_controller import TipoDocumentacionController
from app.decorators.rol_access import rol_access

tipo_documentacion_bp = Blueprint('tipo_documentacion', __name__, url_prefix='/tipos-documentacion')

@tipo_documentacion_bp.route('/', methods=['GET'])
@jwt_required()
@rol_access(["admin", "operador"])
def get_all():
    return TipoDocumentacionController.get_all()

@tipo_documentacion_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@rol_access(["admin", "operador"])
def show(id: int):
    return TipoDocumentacionController.show(id)

@tipo_documentacion_bp.route('/', methods=['POST'])
@jwt_required()
@rol_access(["admin"])
def create():
    return TipoDocumentacionController.create(request.get_json())

@tipo_documentacion_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@rol_access(["admin"])
def update(id: int):
    return TipoDocumentacionController.update(request=request.get_json(), id=id)

@tipo_documentacion_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@rol_access(["admin"])
def destroy(id: int):
    return TipoDocumentacionController.destroy(id)



