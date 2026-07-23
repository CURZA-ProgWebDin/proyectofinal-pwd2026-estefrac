from app.models import db
from app.models.usuario import Usuario
from flask import Response, jsonify
from flask_jwt_extended import create_access_token

class AuthController:


    @staticmethod
    def login(request: dict) -> tuple[Response, int]:

        nombre: str | None = request.get('nombre')
        password: str | None = request.get('password')
        error: str | None = None

        if nombre is None:
            error = "El nombre es requerido"
        if password is None:
            error = "La contraseña es requerida"
        if error is None:
            user = db.session.execute(db.select(Usuario).filter_by(nombre=nombre)).scalar_one_or_none()
            if user and user.validate_password(password):
                access_token = create_access_token(
                    identity=str(user.id),
                    additional_claims={"rol": user.rol.nombre if user.rol else None}
                )
                return jsonify({
                    "access_token": access_token,
                    "rol": user.rol.nombre if user.rol else None,
                    "nombre": user.nombre
                }), 200
            return jsonify({"message": "Credenciales inválidas"}), 401
        return jsonify({"message": error}), 422
