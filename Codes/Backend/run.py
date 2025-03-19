from app import create_app
from app.Routes.Students import students_bp
from flask import jsonify
from flask_cors import CORS
import logging

app = create_app()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:5500", "http://localhost:5500", "null"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

app.register_blueprint(students_bp, url_prefix="/api")

# Add error handler for 500 errors
@app.errorhandler(500)
def handle_500_error(error):
    app.logger.error(f"500 error occurred: {str(error)}")
    return jsonify({
        'error': 'Internal Server Error',
        'message': str(error),
        'status': 500
    }), 500

# Add error handler for 400 errors
@app.errorhandler(400)
def handle_400_error(error):
    app.logger.error(f"400 error occurred: {str(error)}")
    return jsonify({
        'error': 'Bad Request',
        'message': str(error),
        'status': 400
    }), 400

if __name__ == "__main__":
    app.run(debug=True)  # Set to False in production
