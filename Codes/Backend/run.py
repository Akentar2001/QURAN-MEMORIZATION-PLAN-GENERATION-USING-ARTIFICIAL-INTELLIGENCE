from app import create_app

app = create_app()

app.register_blueprint(student_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)  # Set to False in production
