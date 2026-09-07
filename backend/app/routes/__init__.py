from flask import Blueprint

from app.routes.asignacion_routes import asignacion_bp
from app.routes.auth_routes import auth_bp
from app.routes.conductor_routes import conductor_bp
from app.routes.documentacion_vehiculo_routes import documentacion_vehiculo_bp
from app.routes.rol_routes import rol_bp
from app.routes.tipo_documentacion_routes import tipo_documentacion_bp
from app.routes.tipo_vehiculo_routes import tipo_vehiculo_bp
from app.routes.usuario_routes import usuario_bp
from app.routes.vehiculo_routes import vehiculo_bp

api_v1 = Blueprint("api", __name__, url_prefix="/api/v1")
api_v1.register_blueprint(auth_bp)
api_v1.register_blueprint(asignacion_bp)
api_v1.register_blueprint(tipo_vehiculo_bp)
api_v1.register_blueprint(rol_bp)
api_v1.register_blueprint(vehiculo_bp)
api_v1.register_blueprint(usuario_bp)
api_v1.register_blueprint(conductor_bp)
api_v1.register_blueprint(tipo_documentacion_bp)
api_v1.register_blueprint(documentacion_vehiculo_bp)
