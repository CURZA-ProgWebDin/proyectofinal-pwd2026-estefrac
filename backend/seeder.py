from app import create_app
from app.models import db
from app.models.rol import Rol
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    rol_admin = db.session.execute(
        db.select(Rol).filter_by(nombre="admin")
    ).scalar_one_or_none()

    if rol_admin is None:
        rol_admin = Rol(nombre="admin")
        db.session.add(rol_admin)

    rol_operador = db.session.execute(
        db.select(Rol).filter_by(nombre="operador")
    ).scalar_one_or_none()

    if rol_operador is None:
        rol_operador = Rol(nombre="operador")
        db.session.add(rol_operador)

    db.session.flush()

    admin_por_nombre = db.session.execute(
        db.select(Usuario).filter_by(nombre="admin")
    ).scalar_one_or_none()
    admin_por_email = db.session.execute(
        db.select(Usuario).filter_by(email="admin@controlflota.com")
    ).scalar_one_or_none()

    if (
        admin_por_nombre is not None
        and admin_por_email is not None
        and admin_por_nombre.id != admin_por_email.id
    ):
        raise RuntimeError(
            "El nombre y el email del administrador pertenecen a usuarios distintos"
        )

    if admin_por_nombre is None and admin_por_email is not None:
        raise RuntimeError(
            "El email del administrador ya pertenece a otro usuario"
        )

    if admin_por_nombre is not None and admin_por_email is None:
        raise RuntimeError(
            "El nombre del administrador ya pertenece a otro usuario"
        )

    admin = admin_por_nombre

    if admin is None:
        admin = Usuario(
            nombre="admin",
            email="admin@controlflota.com",
            rol_id=rol_admin.id,
            password_hash="",
        )
        admin.generate_password("admin123")
        db.session.add(admin)
    else:
        admin.rol = rol_admin

    db.session.commit()
    print("Seed completado.")
