from flask import Blueprint, request, jsonify
from app.Services.Students_Services import StudentService
from app.models import students_plans_info

students_bp = Blueprint('students', __name__)

@students_bp.route('/add', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        StudentService.create_student(data)
        
        response = {'message': 'Student added successfully'}
        
        return jsonify(response), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/getAll', methods=['GET'])
def get_students():
    try:
        results = StudentService.get_all_students()
        return jsonify({
            'students': [
                {
                    'student_id': student.student_id,
                    'name': student.name,
                    'age': student.age,
                    'gender': student.gender,
                    'nationality': student.nationality,
                    'student_phone': student.student_phone,
                    'parent_phone': student.parent_phone,
                    'notes': student.notes,
                    'user_id': student.user_id,
                    'created_at': student.created_at.isoformat() if student.created_at else None,
                    'updated_at': student.updated_at.isoformat() if student.updated_at else None,
                    'plan_info': {
                        'memorization_direction': plan_info.memorization_direction if plan_info else None,
                        'last_verse_recited': plan_info.last_verse_recited if plan_info else None,
                        'revision_direction': plan_info.revision_direction if plan_info else None,
                        'new_memorization_amount': plan_info.new_memorization_amount if plan_info else None,
                        'small_revision_amount': plan_info.small_revision_amount if plan_info else None,
                        'large_revision_amount': plan_info.large_revision_amount if plan_info else None,
                        'memorization_days': plan_info.memorization_days if plan_info else None,
                        'overall_rating': plan_info.overall_rating if plan_info else None,
                        'memorized_parts': plan_info.memorized_parts if plan_info else None,
                        'created_at': plan_info.created_at.isoformat() if plan_info and plan_info.created_at else None,
                        'updated_at': plan_info.updated_at.isoformat() if plan_info and plan_info.updated_at else None
                    } if plan_info else None
                } for student, plan_info in results
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        student = StudentService.get_student_by_id(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        plan_info = StudentService.get_student_plan_info(student_id)
        
        response = {
            'students': {
                'student_id': student.student_id,
                'name': student.name,
                'age': student.age,
                'gender': student.gender,
                'nationality': student.nationality,
                'student_phone': student.student_phone,
                'parent_phone': student.parent_phone,
                'notes': student.notes,
                'user_id': student.user_id,
                'created_at': student.created_at.isoformat() if student.created_at else None,
                'updated_at': student.updated_at.isoformat() if student.updated_at else None
            }
        }
        
        # Add plan info to response if it exists
        if plan_info:
            response['students']['plan_info'] = {
                'memorization_direction': plan_info.memorization_direction,
                'last_verse_recited': plan_info.last_verse_recited,
                'revision_direction': plan_info.revision_direction,
                'new_memorization_amount': plan_info.new_memorization_amount,
                'small_revision_amount': plan_info.small_revision_amount,
                'large_revision_amount': plan_info.large_revision_amount,
                'memorization_days': plan_info.memorization_days,
                'created_at': plan_info.created_at.isoformat() if plan_info.created_at else None,
                'updated_at': plan_info.updated_at.isoformat() if plan_info.updated_at else None
            }
            
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.get_json()
        student = StudentService.update_student(student_id, data)
        
        # Get the student's plan info if it exists
        plan_info = StudentService.get_student_plan_info(student_id)
        
        response = {
            'message': 'Student updated successfully',
            'student': {
                'student_id': student.student_id,
                'name': student.name,
                'age': student.age,
                'gender': student.gender,
                'nationality': student.nationality,
                'student_phone': student.student_phone,
                'parent_phone': student.parent_phone,
                'notes': student.notes,
                'user_id': student.user_id,
                'created_at': student.created_at.isoformat() if student.created_at else None,
                'updated_at': student.updated_at.isoformat() if student.updated_at else None
            }
        }
        
        # Add plan info to response if it exists
        if plan_info:
            response['student']['plan_info'] = {
                'memorization_direction': plan_info.memorization_direction,
                'last_verse_recited': plan_info.last_verse_recited,
                'revision_direction': plan_info.revision_direction,
                'new_memorization_amount': plan_info.new_memorization_amount,
                'small_revision_amount': plan_info.small_revision_amount,
                'large_revision_amount': plan_info.large_revision_amount,
                'memorization_days': plan_info.memorization_days,
                'created_at': plan_info.created_at.isoformat() if plan_info.created_at else None,
                'updated_at': plan_info.updated_at.isoformat() if plan_info.updated_at else None
            }
            
        return jsonify(response)
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('deleteStudent/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        StudentService.delete_student(student_id)
        return jsonify({'message': 'Student deleted successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
