from flask import Blueprint, request, jsonify
from app.Services.Students_Services import StudentService
from app.Services.students_plans_info_services import StudentPlanInfoService
from app.Services.recitation_session_Service import RecitationSessionService
from datetime import datetime


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
                'overall_rating': plan_info.overall_rating,
                'memorization_days': plan_info.memorization_days,
                'new_memorization_pages_amount': plan_info.new_memorization_pages_amount,
                'large_revision_pages_amount': plan_info.large_revision_pages_amount,
                'small_revision_pages_amount': plan_info.small_revision_pages_amount,
                'memorization_direction': plan_info.memorization_direction,
                'revision_direction': plan_info.revision_direction,
                'last_verse_recited_new_memorization': plan_info.last_verse_recited_new_memorization,
                'last_verse_recited_large_revision': plan_info.last_verse_recited_large_revision,
                'start_surah': plan_info.start_surah,
                'no_verse_in_surah': plan_info.no_verse_in_surah,
                'created_at': plan_info.created_at.isoformat() if plan_info.created_at else None,
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


@students_bp.route('/evaluations', methods=['GET'])
def get_all_students_evaluations():
    try:
        students_list = StudentService.get_all_students()
        today = datetime.now().date()
        fake_date = "2025-04-14"
        response = []

        for student in students_list:
            sessions = RecitationSessionService.get_student_sessions(student_id=student.student_id, date_only=fake_date if fake_date else today)
            
            if not sessions:
                continue
                
            sections = {}
            
            for session in sessions:
                session_data = session[0]
                if session_data.type == 'New_Memorization':
                    section_key = 'memorization'
                elif session_data.type == 'Minor_Revision':
                    section_key = 'minor_review'
                else:
                    section_key = 'major_review'
                
                sections[section_key] = {
                    'session_id': session_data.session_id,
                    'fromS': session.start_surah_name,
                    'fromV': session.start_verse_order,
                    'toS': session.end_surah_name,
                    'toV': session.end_verse_order,
                    'grade': None
                }
            
            if sections:  # Only add students with sessions
                student_data = {
                    'id': student.student_id,
                    'name': student.name,
                    'sections': sections,
                    'attendance_status': 'present'
                }
                response.append(student_data)

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/evaluations', methods=['POST'])
def save_student_evaluation():
    try:
        data = request.get_json()
        student_id = data['student_id']
        is_present = data['attendance_status'] == 'present'
        today = datetime.now().date()
        print(data)
        
        # Get student plan info
        student_plan = StudentPlanInfoService.get_planInfo(student_id)
        if not student_plan:
            return jsonify({'error': 'Student plan not found'}), 404
        for section_type, section_data in data['sections'].items():
            session = RecitationSessionService.get_session(section_data['session_id'])
            
            # Update current session with evaluation data
            update_data = {
                'is_accepted': section_data['is_accepted'],
                'rating': convert_grade_to_rating(section_data['grade']) if is_present else 0
            }
            
            RecitationSessionService.update_session(session.session_id, update_data)
          # Update student's plan based on session type
            
            # If absent or not accepted, update next day's session
            if not is_present or not section_data['is_accepted']:
                next_day = session.date + timedelta(days=1)
                next_day_session = RecitationSessionService.get_student_session_by_date_and_type(
                    student_id, 
                    next_day, 
                    session.type
                )
                
                if next_day_session:
                    update_next_day_data = {
                        'start_verse_id': session.start_verse_id,
                        'end_verse_id': session.end_verse_id,
                        'letters_count': session.letters_count,
                        'pages_count': session.pages_count
                    }
                    RecitationSessionService.update_session(next_day_session.session_id, update_next_day_data)
            
            # Update last verse recited based on session type
            if is_present and section_data['is_accepted']:
                plan_update_data = {}
                if session.type == 'New_Memorization':
                    plan_update_data['last_verse_recited_new_memorization'] = session.end_verse_id
                elif session.type == 'Major_Revision':
                    plan_update_data['last_verse_recited_large_revision'] = session.end_verse_id
                
                if plan_update_data:
                    StudentPlanInfoService.update_planInfo(student_id, plan_update_data)

        # Update student's overall progress and ratings
        StudentPlanInfoService.update_student_progress(student_id)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def convert_grade_to_rating(grade):
    ratings = {
        'ممتاز': 5,
        'جيد جدا': 4,
        'جيد': 3,
        'ضعيف': 2,
        'غير حافظ': 1
    }
    return ratings.get(grade, 0)
