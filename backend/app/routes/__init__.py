from flask import Blueprint
from app.routes.auth_routes import auth_bp

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')
api_v1.register_blueprint(auth_bp)
