from app.models import db, verses
from app.Services.students_plans_info_services import StudentPlanInfoService
from app.Services.recitation_session_Service import RecitationSessionService

class ManageRecitationEvaluationService:
    RATING_FIELDS = {
        'New_Memorization': 'overall_rating_new_memorization',
        'Major_Revision': 'overall_rating_large_revision',
        'Minor_Revision': 'overall_rating_small_revision'
    }

    @staticmethod
    def _get_verse_id(surah_id, verse_order):
        verse = verses.query.filter_by(surah_id=surah_id, order_in_surah=verse_order).first()
        return verse.verse_id if verse else None

    @staticmethod
    def _update_section_rating(student_plan, session, section_data):
        old_rate = session.rating or 0
        new_rate = section_data['grade'] or 0
        
        section_sessions_count = RecitationSessionService.get_student_sessions_count(
            student_id=student_plan.student_id,
            recitation_type=session.type,
            is_rating_not_none=True
        )
        
        current_rating = getattr(student_plan, ManageRecitationEvaluationService.RATING_FIELDS[session.type]) or 0
        sum_old_section_rating = (current_rating * section_sessions_count) - old_rate + new_rate
        
        if not session.rating:
            section_sessions_count += 1
            
        return {
            'new_rate': new_rate,
            'old_rate': old_rate,
            'rating_value': sum_old_section_rating / section_sessions_count if section_sessions_count > 0 else 0
        }

    @staticmethod
    def _prepare_session_update(section_data):
        update_data = {
            'is_accepted': section_data['is_accepted'],
            'rating': section_data['grade']
        }
        
        from_verse_id = ManageRecitationEvaluationService._get_verse_id(
            section_data['fromSurah'],
            section_data['fromVerse']
        )
        to_verse_id = ManageRecitationEvaluationService._get_verse_id(
            section_data['toSurah'],
            section_data['toVerse']
        )
        
        if from_verse_id:
            update_data['fromVerse'] = from_verse_id
        if to_verse_id:
            update_data['toVerse'] = to_verse_id
            
        return update_data

    @staticmethod
    def evaluate_sessions(student_id, data):
        try:            
            student_plan = StudentPlanInfoService.get_planInfo(student_id)
            if not student_plan:
                raise Exception('Student plan not found')
    
            sessions_count = RecitationSessionService.get_student_sessions_count(student_id, is_rating_not_none=True)
            sum_old_overall_rating = (student_plan.overall_rating or 0) * sessions_count
            plan_update_data = {}
            
            for section_type, section_data in data['sections'].items():
                session = RecitationSessionService.get_session(section_data['session_id'])
                
                rating_update = ManageRecitationEvaluationService._update_section_rating(
                    student_plan, session, section_data
                )
                sum_old_overall_rating += rating_update['new_rate'] - rating_update['old_rate']
                plan_update_data[ManageRecitationEvaluationService.RATING_FIELDS[session.type]] = rating_update['rating_value']

                update_data = ManageRecitationEvaluationService._prepare_session_update(section_data)
                RecitationSessionService.update_session(session.session_id, update_data)
                
                if section_data['is_accepted']:
                    if session.type == 'New_Memorization':
                        plan_update_data['last_verse_recited_new_memorization'] = session.end_verse_id
                    elif session.type == 'Major_Revision':
                        plan_update_data['last_verse_recited_large_revision'] = session.end_verse_id
                else:
                    if session.type == 'New_Memorization':
                        ManageRecitationEvaluationService.shift_subsequent_sessions_verses(student_id, session)
                        minor_rev_session = RecitationSessionService.get_student_sessions(student_id=student_id, recitation_type='Minor_Revision', date_only=session.date)
                        if minor_rev_session:
                            minor_rev_session = minor_rev_session[0][0]
                            ManageRecitationEvaluationService.shift_subsequent_sessions_verses(student_id, minor_rev_session, after_date=session.date)
                        else:
                            ManageRecitationEvaluationService.shift_subsequent_sessions_verses(student_id, minor_rev_session, after_date=session.date)
                    elif session.type == 'Major_Revision':
                        ManageRecitationEvaluationService.shift_subsequent_sessions_verses(student_id, session)
                    elif session.type == 'Minor_Revision':
                        ManageRecitationEvaluationService.shift_subsequent_sessions_verses(student_id, session, isMinorRevision=True)           

            new_sessions_count = RecitationSessionService.get_student_sessions_count(student_id, is_rating_not_none=True)
            plan_update_data['overall_rating'] = sum_old_overall_rating / new_sessions_count  if new_sessions_count > 0 else 0
            
            if plan_update_data:
                StudentPlanInfoService.update_planInfo(student_id, plan_update_data)
            
            return True
        except Exception as e:
            raise e

    @staticmethod
    def shift_subsequent_sessions_verses(student_id, session, isMinorRevision=False, after_date=None):
        try:
            if not session:
                if after_date:
                    subsequent_sessions = RecitationSessionService.get_student_sessions(
                        student_id=student_id,
                        recitation_type='Minor_Revision', 
                        start_date=after_date,
                        ascending=True
                    )
                    if not subsequent_sessions or not subsequent_sessions[0]:
                        raise Exception('No subsequent sessions found after date')
                    
                    current_start_verse = subsequent_sessions[0][0].start_verse_id
                    current_end_verse = subsequent_sessions[0][0].end_verse_id
                    RecitationSessionService.delete_session(subsequent_sessions[0][0].session_id)
                else:
                    raise Exception('Session not found')
            
            else:
                subsequent_sessions = RecitationSessionService.get_student_sessions(
                    student_id=student_id,
                    recitation_type=session.type, 
                    after_session=session.session_id,
                    ascending=True
                )
                current_start_verse = session.start_verse_id
                current_end_verse = session.end_verse_id
            
            if not subsequent_sessions:
                return True
            for sess in subsequent_sessions:
                if not session and after_date and sess == subsequent_sessions[0]:
                    continue

                current_session = sess[0]
                
                if current_start_verse == current_session.start_verse_id and current_end_verse == current_session.end_verse_id:
                    return True
                
                if isMinorRevision:
                    current_session.start_verse_id = current_start_verse
                    db.session.commit()
                    return True

                next_start_verse = current_session.start_verse_id
                next_end_verse = current_session.end_verse_id
                
                current_session.start_verse_id = current_start_verse
                current_session.end_verse_id = current_end_verse
                
                current_start_verse = next_start_verse
                current_end_verse = next_end_verse

            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error shifting session verses: {str(e)}")