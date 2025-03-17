from flask import Blueprint, request, jsonify
from models.plan import Plan
from db import get_db_connection

plan_bp = Blueprint('plan', __name__)

@plan_bp.route('/plans', methods=['GET'])
def get_plans():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    plans = Plan.get_all(conn)
    conn.close()
    
    if plans is None:
        return jsonify({"error": "Failed to retrieve plans"}), 500
    
    return jsonify(plans)

@plan_bp.route('/plans/<int:plan_id>', methods=['GET'])
def get_plan(plan_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    plan = Plan.get_by_id(conn, plan_id)
    conn.close()
    
    if plan is None:
        return jsonify({"error": "Plan not found"}), 404
    
    return jsonify(plan)

@plan_bp.route('/students/<int:student_id>/plans', methods=['GET'])
def get_student_plans(student_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    plans = Plan.get_by_student(conn, student_id)
    conn.close()
    
    if plans is None:
        return jsonify({"error": "Failed to retrieve plans"}), 500
    
    return jsonify(plans)

@plan_bp.route('/plans', methods=['POST'])
def add_plan():
    if not request.json:
        return jsonify({"error": "Invalid request data"}), 400
    
    data = request.json
    required_fields = ['StudentID', 'StartDate', 'EndDate', 'Status']
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    plan_id = Plan.create(conn, data)
    conn.close()
    
    if plan_id is None:
        return jsonify({"error": "Failed to create plan"}), 500
    
    return jsonify({"message": "Plan added successfully", "id": plan_id}), 201

@plan_bp.route('/plans/<int:plan_id>', methods=['PUT'])
def update_plan(plan_id):
    if not request.json:
        return jsonify({"error": "Invalid request data"}), 400
    
    data = request.json
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    # Check if plan exists
    plan = Plan.get_by_id(conn, plan_id)
    if plan is None:
        conn.close()
        return jsonify({"error": "Plan not found"}), 404
    
    success = Plan.update(conn, plan_id, data)
    conn.close()
    
    if not success:
        return jsonify({"error": "Failed to update plan"}), 500
    
    return jsonify({"message": "Plan updated successfully"})

@plan_bp.route('/plans/<int:plan_id>', methods=['DELETE'])
def delete_plan(plan_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    # Check if plan exists
    plan = Plan.get_by_id(conn, plan_id)
    if plan is None:
        conn.close()
        return jsonify({"error": "Plan not found"}), 404
    
    success = Plan.delete(conn, plan_id)
    conn.close()
    
    if not success:
        return jsonify({"error": "Failed to delete plan"}), 500
    
    return jsonify({"message": "Plan deleted successfully"})