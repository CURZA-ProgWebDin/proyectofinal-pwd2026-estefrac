from app.controllers import Controller
from app.models import db
from app.models.usuario import Usuario
from app.models.rol import Rol
from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError

class UsuarioController(Controller):
    @staticmethod
    def get_all() -> tuple[Response, int]:
        usuarios = db.session.execute(
            db.select(Usuario).order_by(db.desc(Usuario.id))
        ).scalars().all()

        if usuarios:
            return jsonify([usuario.to_dict() for usuario in usuarios]), 200

        return jsonify({"message": "No se encontraron usuarios"}), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        usuario = db.session.get(Usuario, id)

        if usuario:
            return jsonify(usuario.to_dict()), 200

        return jsonify({"message": "Usuario no encontrado"}), 404

    @staticmethod
    def create(request: dict) -> tuple[Response, int]:
        nombre: str | None = request.get("nombre")
        email: str | None = request.get("email")
        password: str | None = request.get("password")
        rol_id: int | None = request.get("rol_id")

        if nombre is None:
            return jsonify({"message": "El nombre es requerido"}), 422

        if email is None:
            return jsonify({"message": "El email es requerido"}), 422

        if password is None:
            return jsonify({"message": "La contraseña es requerida"}), 422

        if rol_id is None:
            return jsonify({"message": "El rol es requerido"}), 422

        rol = db.session.get(Rol, rol_id)

        if rol is None or rol.activo != "S":
            return jsonify({"message": "El rol no existe o no está activo"}), 422

        try:
            usuario = Usuario(
                nombre=nombre, email=email, rol_id=rol_id, password_hash=""
            )
            usuario.generate_password(password)

            db.session.add(usuario)
            db.session.commit()

            return jsonify({"message": "Usuario creado exitosamente"}), 201

        except IntegrityError:
            db.session.rollback()

            return jsonify({"message": "El nombre o email ya existe"}), 409

    @staticmethod
    def update(request: dict, id: int) -> tuple[Response, int]:
        nombre: str | None = request.get("nombre")
        email: str | None = request.get("email")
        password: str | None = request.get("password")
        rol_id: int | None = request.get("rol_id")
        activo: str | None = request.get("activo")

        
        if nombre is None:
            return jsonify({"message": "El nombre es requerido"}), 422

        if email is None:
            return jsonify({"message": "El email es requerido"}), 422

        if rol_id is None:
            return jsonify({"message": "El rol es requerido"}), 422

        if activo is None:
            return jsonify({"message": "El estado activo es requerido"}), 422

        if activo not in ["S", "N"]:
            return jsonify({"message": "El estado activo debe ser 'S' o 'N'"}), 422

        usuario = db.session.get(Usuario, id)

        if usuario is None:
            return jsonify({"message": "Usuario no encontrado"}), 404

        rol = db.session.get(Rol, rol_id)

        if rol is None or rol.activo != "S":
            return jsonify({"message": "El rol no existe o no está activo"}), 422

        try:
            usuario.nombre = nombre
            usuario.email = email
            usuario.rol_id = rol_id
            usuario.activo = activo

            if password is not None:
                usuario.generate_password(password)

            db.session.commit()

            return jsonify({"message": "Usuario actualizado exitosamente"}), 200

        except IntegrityError:
            db.session.rollback()

            return jsonify({"message": "El nombre o email ya existe"}), 409

    @staticmethod
    def destroy(id: int) -> tuple[Response, int]:
        usuario = db.session.get(Usuario, id)

        if usuario is None:
            return jsonify({"message": "Usuario no encontrado"}), 404

        usuario.activo = "N"
        db.session.commit()

        return jsonify({"message": "Usuario desactivado exitosamente"}), 200
