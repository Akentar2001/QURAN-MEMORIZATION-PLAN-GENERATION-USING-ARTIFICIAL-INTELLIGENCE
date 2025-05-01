from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config import Config
from flask_cors import CORS

# Initialize extensions without binding to app
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
        
    db.init_app(app)  # Ensure this line exists
    
   
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://127.0.0.1:5500", "http://localhost:5500", "null"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Initialize extensions with app
    
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.Routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app