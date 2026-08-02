from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import db
from app.models.usuario import Usuario

def rol_access(roles_permitidos):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()

            usuario = db.session.execute( db.select(Usuario).filter_by(id=user_id) ).scalar_one_or_none()

            if (
                usuario
                and usuario.activo == "S"
                and usuario.rol
                and usuario.rol.activo == "S"
                and usuario.rol.nombre in roles_permitidos
            ):
                return func(*args, **kwargs)

            return jsonify({"message": "Acceso denegado"}), 403

        return wrapper
    return decorator
