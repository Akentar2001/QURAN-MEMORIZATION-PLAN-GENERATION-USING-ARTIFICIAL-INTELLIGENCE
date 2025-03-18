from flask import Blueprint, jsonify
from app.models import db, User  # Import models

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({"message": "Flask API is working!"})

@main.route("/users")
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name} for user in users])
