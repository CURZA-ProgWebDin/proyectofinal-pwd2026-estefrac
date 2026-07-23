import os
from flask import Flask
from app.config import config
from app.models import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.routes import api_v1

migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    app.register_blueprint(api_v1)
    return app
