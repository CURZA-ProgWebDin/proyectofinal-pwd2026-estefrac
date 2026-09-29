from flask import Response, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity

from app.models import db
from app.models.usuario import Usuario


class AuthController:
    @staticmethod
    def login(request: dict) -> tuple[Response, int]:

        nombre: str | None = request.get("nombre")
        password: str | None = request.get("password")

        if nombre is None:
            return jsonify({"message": "El nombre es requerido"}), 422

        if password is None:
            return jsonify({"message": "La contraseña es requerida"}), 422

        user = db.session.execute(
            db.select(Usuario).filter_by(nombre=nombre)
        ).scalar_one_or_none()

        if user and user.activo == "S" and user.validate_password(password):
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"rol": user.rol.nombre if user.rol else None},
            )
            return jsonify(
                {
                    "access_token": access_token,
                    "rol": user.rol.nombre if user.rol else None,
                    "nombre": user.nombre,
                }
            ), 200

        return jsonify({"message": "Credenciales inválidas"}), 401

    @staticmethod
    def me() -> tuple[Response, int]:
        user_id = get_jwt_identity()

        user = db.session.execute(
            db.select(Usuario).filter_by(id=user_id)
        ).scalar_one_or_none()

        if user and user.activo != "S":
            return jsonify({"message": "Acceso denegado"}), 403

        if user:
            return jsonify(
                {
                    "id": user.id,
                    "nombre": user.nombre,
                    "email": user.email,
                    "rol": user.rol.nombre if user.rol else None,
                }
            ), 200
        return jsonify({"message": "Usuario no encontrado"}), 404
