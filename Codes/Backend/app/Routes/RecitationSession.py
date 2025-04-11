from flask import Blueprint, request, jsonify
from app.Services.recitation_session_Service import RecitationSessionService
from app.Services.Students_Services import StudentService

recitation_session_bp = Blueprint('recitation_session', __name__)

@recitation_session_bp.route('/sessions', methods=['POST'])
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

@recitation_session_bp.route('/sessions/<int:session_id>', methods=['GET'])
def get_session(session_id):
    try:
        session_data = RecitationSessionService.get_session(session_id)
        if not session_data:
            return jsonify({'error': 'Session not found'}), 404
            
        return jsonify({
            'session_id': session_data[0].session_id,
            'student_id': session_data[0].student_id,
            'date': session_data[0].date,
            'type': session_data[0].type,
            'start_verse': {
                'verse_id': session_data[0].start_verse_id,
                'surah_name': session_data[0].start_surah_name,
                'order_in_surah': session_data[0].start_verse_order
            },
            'end_verse': {
                'verse_id': session_data[0].end_verse_id,
                'surah_name': session_data[0].end_surah_name,
                'order_in_surah': session_data[0].end_verse_order
            },
            'rating': session_data[0].rating,
            'is_accepted': session_data[0].is_accepted,
            'pages_count': session_data[0].pages_count,
            'letters_count': session_data[0].letters_count,
            'rl_reward_signal': session_data[0].rl_reward_signal
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 404

@recitation_session_bp.route('/sessions/student/<int:student_id>', methods=['GET'])

def get_student_sessions(student_id):
    try:
        student = StudentService.get_student_by_id(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        sessions = RecitationSessionService.get_student_sessions(student_id)

        if not sessions:
            return jsonify({'message': 'No sessions found for this student'})

        return jsonify([{
            'session_id': session[0].session_id,
            'student_id': session[0].student_id,
            'date': session[0].date,
            'type': session[0].type,
            'start_verse': {
                'verse_id': session[0].start_verse_id,
                'surah_name': session[0].start_surah_name,
                'order_in_surah': session[0].start_verse_order
            },
            'end_verse': {
                'verse_id': session[0].end_verse_id,
                'surah_name': session[0].end_surah_name,
                'order_in_surah': session[0].end_verse_order
            },
            'rating': session[0].rating,
            'is_accepted': session[0].is_accepted,
            'pages_count': session[0].pages_count,
            'letters_count': session[0].letters_count,
            'rl_reward_signal': session[0].rl_reward_signal
        } for session in sessions]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@recitation_session_bp.route('/sessions/<int:session_id>', methods=['PUT'])
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

@recitation_session_bp.route('/sessions/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    try:
        RecitationSessionService.delete_session(session_id)
        return jsonify({
            'message': 'Session deleted successfully'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400