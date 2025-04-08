from flask import Blueprint, request, jsonify
from app.Services.Students_Services import StudentService
from app.Services.students_plans_info_services import StudentPlanInfoService

students_bp = Blueprint('students', __name__)

@students_bp.route('/add', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        student = StudentService.create_student(data)

        response = {
            'message': 'Student added successfully',
            'student': {
                'student_id': student.student_id,
                'name': student.name,
                'age': student.age,
                'gender': student.gender,
                'nationality': student.nationality,
                'student_phone': student.student_phone,
                'parent_phone': student.parent_phone,
                'notes': student.notes,
                'created_at': student.created_at.isoformat() if student.created_at else None,
                'updated_at': student.updated_at.isoformat() if student.updated_at else None
            }
        }

        return jsonify(response), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/getAll', methods=['GET'])
def get_students():
    try:
        students = StudentService.get_all_students()
        response = {
            'students': []
        }

        for student in students:
            plan_info = StudentPlanInfoService.get_planInfo(student.student_id)
            student_data = {
                'student_id': student.student_id,
                'name': student.name,
                'age': student.age,
                'gender': student.gender,
                'created_at': student.created_at.isoformat() if student.created_at else None,
                'updated_at': student.updated_at.isoformat() if student.updated_at else None,
                'plan_info': {
                    'memorized_parts': plan_info.memorized_parts,
                    'overall_rating': plan_info.overall_rating,
                    'created_at': plan_info.created_at.isoformat() if plan_info.created_at else None,
                    'updated_at': plan_info.updated_at.isoformat() if plan_info.updated_at else None
                } if plan_info else None
            }
            response['students'].append(student_data)

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/getUserStudents/<int:user_id>', methods=['GET'])
def get_user_students(user_id):
    try:
        students = StudentService.get_user_students(user_id)
        response = {
            'students': []
        }

        for student in students:
            plan_info = StudentPlanInfoService.get_planInfo(student.student_id)
            student_data = {
                'student_id': student.student_id,
                'name': student.name,
                'age': student.age,
                'gender': student.gender,
                'created_at': student.created_at.isoformat() if student.created_at else None,
                'updated_at': student.updated_at.isoformat() if student.updated_at else None,
                'plan_info': {
                    'memorized_parts': plan_info.memorized_parts,
                    'overall_rating': plan_info.overall_rating,
                    'created_at': plan_info.created_at.isoformat() if plan_info.created_at else None,
                    'updated_at': plan_info.updated_at.isoformat() if plan_info.updated_at else None
                } if plan_info else None
            }
            response['students'].append(student_data)

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/getStudent/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        student = StudentService.get_student_by_id(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
            
        plan_info = StudentPlanInfoService.get_planInfo(student_id)
        response = {
            'student_id': student.student_id,
            'name': student.name,
            'age': student.age,
            'gender': student.gender,
            'nationality': student.nationality,
            'student_phone': student.student_phone,
            'parent_phone': student.parent_phone,
            'notes': student.notes,
            'plan_info': {
                'memorized_parts': plan_info.memorized_parts,
                'memorization_direction': plan_info.memorization_direction,
                'revision_direction': plan_info.revision_direction,
                'memorization_days': plan_info.memorization_days,
                'overall_rating': plan_info.overall_rating,
                'updated_at': plan_info.updated_at.isoformat() if plan_info.updated_at else None
            } if plan_info else None
        }
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('update/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.get_json()
        student = StudentService.update_student(student_id, data)
        
        response = {
            'message': 'Student updated successfully',
            'student': {
                'student_id': student.student_id,
                'name': student.name
            }
        }
        return jsonify(response), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/delete/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        StudentService.delete_student(student_id)
        return jsonify({'message': 'Student deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
