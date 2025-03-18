from flask import Blueprint

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return {"message": "Flask PostgreSQL API is running!"}
