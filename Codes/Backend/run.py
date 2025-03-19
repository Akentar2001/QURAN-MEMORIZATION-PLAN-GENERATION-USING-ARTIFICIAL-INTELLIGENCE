from app import create_app
from app.Routes.Students import students_bp

app = create_app()

app.register_blueprint(students_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)  # Set to False in production
