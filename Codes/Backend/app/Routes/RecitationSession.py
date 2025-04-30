from flask import Blueprint, request, jsonify
from app.Services.recitation_session_Service import RecitationSessionService
from app.Services.Students_Services import StudentService
from app.Services.students_plans_info_services import StudentPlanInfoService
from app.Services.manage_recitation_evaluation_service import ManageRecitationEvaluationService
from datetime import datetime

recitation_session_bp = Blueprint('recitation_session', __name__)

@recitation_session_bp.route('/getSession', methods=['POST'])
def create_session():
    try:
        data = request.get_json()
        
        student = StudentService.get_student(data['student_id'])
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        session = RecitationSessionService.create_session(data)
        return jsonify({
            'message': 'Session created successfully',
            'session_id': session.session_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@recitation_session_bp.route('/get/<int:session_id>', methods=['GET'])
def get_session(session_id):
    try:
        session_data = RecitationSessionService.get_session(session_id)
        return jsonify({
            'session_id': session_data[0].session_id,
            'student_id': session_data[0].student_id,
            'date': session_data[0].date,
            'type': session_data[0].type,
            'start_verse': {
                'verse_id': session_data[0].start_verse_id,
                'surah_name': session_data.start_surah_name,
                'order_in_surah': session_data.start_verse_order
            },
            'end_verse': {
                'verse_id': session_data[0].end_verse_id,
                'surah_name': session_data.end_surah_name,
                'order_in_surah': session_data.end_verse_order
            },
            'rating': session_data[0].rating,
            'is_accepted': session_data[0].is_accepted,
            'pages_count': session_data[0].pages_count,
            'letters_count': session_data[0].letters_count,
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 404

@recitation_session_bp.route('/getSessions/student/<int:student_id>', methods=['GET'])

def get_student_sessions(student_id):
    try:
        student = StudentService.get_student_by_id(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        sessions = RecitationSessionService.get_student_sessions(student_id=student_id)

        if not sessions:
            return jsonify({'message': 'No sessions found for this student'})

        return jsonify([{
            'session_id': session[0].session_id,
            'student_id': session[0].student_id,
            'date': session[0].date,
            'type': session[0].type,
            'start_verse': {
                'verse_id': session[0].start_verse_id,
                'surah_name': session.start_surah_name,
                'order_in_surah': session.start_verse_order
            },
            'end_verse': {
                'verse_id': session[0].end_verse_id,
                'surah_name': session.end_surah_name,
                'order_in_surah': session.end_verse_order
            },
            'rating': session[0].rating,
            'is_accepted': session[0].is_accepted,
            'pages_count': session[0].pages_count,
            'letters_count': session[0].letters_count,
        } for session in sessions]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@recitation_session_bp.route('/updateSession/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    try:
        data = request.get_json()
        session = RecitationSessionService.update_session(session_id, data)
        return jsonify({
            'message': 'Session updated successfully',
            'session_id': session.session_id
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@recitation_session_bp.route('/deleteSession/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    try:
        RecitationSessionService.delete_session(session_id)
        return jsonify({
            'message': 'Session deleted successfully'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@recitation_session_bp.route('/getAllSessionsStudents', methods=['GET'])
def get_all_students_sessions():
    try:
        students_list = StudentService.get_all_students()
        today = datetime.now().date()
        fake_date = "2025-03-02"  #! Put the date of the sessions you want to get, Default is today
        date = fake_date if fake_date else today

        response = []

        for student in students_list:
            sessions = RecitationSessionService.get_student_sessions(student_id=student.student_id, date_only=date)
            
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
                    'grade': session_data.rating if session_data.rating else None
                }
            
            if sections:
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


@recitation_session_bp.route('/updateSessions/student/<int:student_id>', methods=['PUT'])
def save_student_Sessions_evaluation(student_id):
    try:
        data = request.get_json()
        ManageRecitationEvaluationService.evaluate_sessions(student_id, data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500