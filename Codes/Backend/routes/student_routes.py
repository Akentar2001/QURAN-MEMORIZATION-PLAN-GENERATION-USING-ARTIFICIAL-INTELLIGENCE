from flask import Blueprint, request, jsonify
from models.student import Student
from db import get_db_connection

student_bp = Blueprint('student', __name__)

@student_bp.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    students = Student.get_all(conn)
    conn.close()
    
    if students is None:
        return jsonify({"error": "Failed to retrieve students"}), 500
    
    return jsonify(students)

@student_bp.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    student = Student.get_by_id(conn, student_id)
    conn.close()
    
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    
    return jsonify(student)

@student_bp.route('/students', methods=['POST'])
def add_student():
    if not request.json:
        return jsonify({"error": "Invalid request data"}), 400
    
    data = request.json
    required_fields = ['Name', 'Age', 'Level', 'PhoneNumber']
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    student_id = Student.create(conn, data)
    conn.close()
    
    if student_id is None:
        return jsonify({"error": "Failed to create student"}), 500
    
    return jsonify({"message": "Student added successfully", "id": student_id}), 201

@student_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    if not request.json:
        return jsonify({"error": "Invalid request data"}), 400
    
    data = request.json
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    # Check if student exists
    student = Student.get_by_id(conn, student_id)
    if student is None:
        conn.close()
        return jsonify({"error": "Student not found"}), 404
    
    success = Student.update(conn, student_id, data)
    conn.close()
    
    if not success:
        return jsonify({"error": "Failed to update student"}), 500
    
    return jsonify({"message": "Student updated successfully"})

@student_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    # Check if student exists
    student = Student.get_by_id(conn, student_id)
    if student is None:
        conn.close()
        return jsonify({"error": "Student not found"}), 404
    
    success = Student.delete(conn, student_id)
    conn.close()
    
    if not success:
        return jsonify({"error": "Failed to delete student"}), 500
    
    return jsonify({"message": "Student deleted successfully"})