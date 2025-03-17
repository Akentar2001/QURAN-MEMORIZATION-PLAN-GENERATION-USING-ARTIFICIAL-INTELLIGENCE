from flask import Blueprint, request, jsonify
from models.evaluation import Evaluation
from db import get_db_connection

evaluation_bp = Blueprint('evaluation', __name__)

@evaluation_bp.route('/evaluations', methods=['GET'])
def get_evaluations():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    evaluations = Evaluation.get_all(conn)
    conn.close()
    
    if evaluations is None:
        return jsonify({"error": "Failed to retrieve evaluations"}), 500
    
    return jsonify(evaluations)

@evaluation_bp.route('/evaluations/<int:evaluation_id>', methods=['GET'])
def get_evaluation(evaluation_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    evaluation = Evaluation.get_by_id(conn, evaluation_id)
    conn.close()
    
    if evaluation is None:
        return jsonify({"error": "Evaluation not found"}), 404
    
    return jsonify(evaluation)

@evaluation_bp.route('/students/<int:student_id>/evaluations', methods=['GET'])
def get_student_evaluations(student_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    evaluations = Evaluation.get_by_student(conn, student_id)
    conn.close()
    
    if evaluations is None:
        return jsonify({"error": "Failed to retrieve evaluations"}), 500
    
    return jsonify(evaluations)

@evaluation_bp.route('/evaluations', methods=['POST'])
def add_evaluation():
    if not request.json:
        return jsonify({"error": "Invalid request data"}), 400
    
    data = request.json
    required_fields = ['StudentID', 'Date', 'Score', 'Notes']
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    evaluation_id = Evaluation.create(conn, data)
    conn.close()
    
    if evaluation_id is None:
        return jsonify({"error": "Failed to create evaluation"}), 500
    
    return jsonify({"message": "Evaluation added successfully", "id": evaluation_id}), 201

@evaluation_bp.route('/evaluations/<int:evaluation_id>', methods=['PUT'])
def update_evaluation(evaluation_id):
    if not request.json:
        return jsonify({"error": "Invalid request data"}), 400
    
    data = request.json
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    # Check if evaluation exists
    evaluation = Evaluation.get_by_id(conn, evaluation_id)
    if evaluation is None:
        conn.close()
        return jsonify({"error": "Evaluation not found"}), 404
    
    success = Evaluation.update(conn, evaluation_id, data)
    conn.close()
    
    if not success:
        return jsonify({"error": "Failed to update evaluation"}), 500
    
    return jsonify({"message": "Evaluation updated successfully"})

@evaluation_bp.route('/evaluations/<int:evaluation_id>', methods=['DELETE'])
def delete_evaluation(evaluation_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    # Check if evaluation exists
    evaluation = Evaluation.get_by_id(conn, evaluation_id)
    if evaluation is None:
        conn.close()
        return jsonify({"error": "Evaluation not found"}), 404
    
    success = Evaluation.delete(conn, evaluation_id)
    conn.close()
    
    if not success:
        return jsonify({"error": "Failed to delete evaluation"}), 500
    
    return jsonify({"message": "Evaluation deleted successfully"})