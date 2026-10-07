from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.controllers.dashboard_controller import DashboardController
from app.decorators.rol_access import rol_access

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/", methods=["GET"])
@jwt_required()
@rol_access(["admin", "operador"])
def get_resumen():
    return DashboardController.get_resumen()
