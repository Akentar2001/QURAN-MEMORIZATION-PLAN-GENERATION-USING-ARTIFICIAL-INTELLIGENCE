from app import create_app
from app.Routes.Students import students_bp
from app.Routes.RecitationSession import recitation_session_bp
from flask import jsonify
from flask_cors import CORS
import logging

app = create_app()

logging.basicConfig(level=logging.DEBUG)

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:5500", "http://localhost:5500", "null"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

app.register_blueprint(students_bp, url_prefix="/api/students")
app.register_blueprint(recitation_session_bp, url_prefix="/api/recitation_session")

@app.errorhandler(500)
def handle_500_error(error):
    app.logger.error(f"500 error occurred: {str(error)}")
    return jsonify({
        'error': 'Internal Server Error',
        'message': str(error),
        'status': 500
    }), 500

@app.errorhandler(400)
def handle_400_error(error):
    app.logger.error(f"400 error occurred: {str(error)}")
    return jsonify({
        'error': 'Bad Request',
        'message': str(error),
        'status': 400
    }), 400

if __name__ == "__main__":
    app.run(debug=True)
