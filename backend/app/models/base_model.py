from . import db

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    activo = db.Column(db.String(1), nullable=False, default="S")
    creado_en = db.Column(db.DateTime, server_default=db.func.now())
    actualizado_en = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "creado_en": self.creado_en.isoformat() if self.creado_en else None,
            "actualizado_en": self.actualizado_en.isoformat() if self.actualizado_en else None,
            "activo": self.activo
        }
