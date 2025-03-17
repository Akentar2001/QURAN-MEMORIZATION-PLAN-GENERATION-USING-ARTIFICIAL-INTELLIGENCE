from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import mysql.connector
from mysql.connector import Error
from routes.student_routes import student_bp
from routes.plan_routes import plan_bp
from routes.evaluation_routes import evaluation_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(student_bp, url_prefix='/api')
app.register_blueprint(plan_bp, url_prefix='/api')
app.register_blueprint(evaluation_bp, url_prefix='/api')

# Database connection function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Add your MySQL password here
            database='quran_memorization'
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

# Test route
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working!"})

# Student routes
@app.route('/api/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Students')
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(students)

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Students WHERE StudentID = %s', (student_id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    
    return jsonify(student)

@app.route('/api/students', methods=['POST'])
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
    
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO Students (Name, Age, Level, PhoneNumber)
            VALUES (%s, %s, %s, %s)
        ''', (data['Name'], data['Age'], data['Level'], data['PhoneNumber']))
        
        conn.commit()
        student_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Student added successfully", "id": student_id}), 201
    
    except Error as e:
        cursor.close()
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    if not request.json:
        return jsonify({"error": "Invalid request data"}), 400
    
    data = request.json
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Check if student exists
    cursor.execute('SELECT * FROM Students WHERE StudentID = %s', (student_id,))
    student = cursor.fetchone()
    if student is None:
        cursor.close()
        conn.close()
        return jsonify({"error": "Student not found"}), 404
    
    # Update fields that are provided
    fields = []
    values = []
    
    for field in ['Name', 'Age', 'Level', 'PhoneNumber']:
        if field in data:
            fields.append(f"{field} = %s")
            values.append(data[field])
    
    if not fields:
        cursor.close()
        conn.close()
        return jsonify({"error": "No fields to update"}), 400
    
    values.append(student_id)
    
    try:
        cursor.execute(f'''
            UPDATE Students
            SET {", ".join(fields)}
            WHERE StudentID = %s
        ''', values)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Student updated successfully"})
    
    except Error as e:
        cursor.close()
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Check if student exists
    cursor.execute('SELECT * FROM Students WHERE StudentID = %s', (student_id,))
    student = cursor.fetchone()
    if student is None:
        cursor.close()
        conn.close()
        return jsonify({"error": "Student not found"}), 404
    
    try:
        cursor.execute('DELETE FROM Students WHERE StudentID = %s', (student_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Student deleted successfully"})
    
    except Error as e:
        cursor.close()
        conn.close()
        return jsonify({"error": str(e)}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=9000)