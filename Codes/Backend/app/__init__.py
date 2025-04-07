from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config import Config
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS to allow requests from your frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://127.0.0.1:5500", "http://localhost:5500", "null"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate

    from app.Routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app