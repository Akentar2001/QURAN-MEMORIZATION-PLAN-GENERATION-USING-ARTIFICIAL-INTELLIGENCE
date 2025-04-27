from datetime import date
from app.models import db, recitation_session, verses, surahs
from sqlalchemy.orm import aliased
from sqlalchemy import func, cast, Date
from app.Services.students_plans_info_services import StudentPlanInfoService

class RecitationSessionService:
    @staticmethod
    def create_session(data):
        try:
            new_session = recitation_session(
                student_id=data['student_id'],
                date=data['date'] if 'date' in data else date.today(),
                type=data['type'],
                start_verse_id=data['start_verse_id'],
                end_verse_id=data['end_verse_id'],
                letters_count=data['letters_count']
            )
            if 'is_accepted' in data:
                new_session.is_accepted = data['is_accepted']
            if 'rating' in data:
                new_session.rating = data['rating']
            if 'pages_count' in data:
                new_session.pages_count = data['pages_count']
            
            db.session.add(new_session)
            db.session.commit()
            return new_session
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error creating session: {str(e)}")
        finally:
            db.session.close()

    @staticmethod
    def get_session(session_id):
        return recitation_session.query.get_or_404(session_id)

    @staticmethod
    def get_student_sessions(student_id, recitation_type=None, limit_count=None, start_date=None, end_date=None, date_only=None, is_accepted=None, is_accepted_not_none=None, is_rating_not_none=None):
        StartVerse = aliased(verses)
        EndVerse = aliased(verses)
        StartSurah = aliased(surahs)
        EndSurah = aliased(surahs)

        query = (recitation_session.query
            .filter_by(student_id=student_id))

        if is_accepted is not None:
            query = query.filter_by(is_accepted=is_accepted)
        elif is_accepted_not_none:
            query = query.filter(recitation_session.is_accepted.isnot(None))
        elif is_accepted_not_none is False:
            query = query.filter(recitation_session.is_accepted.is_(None))

        if is_rating_not_none:
            query = query.filter(recitation_session.rating.isnot(None))

        if recitation_type:
            query = query.filter_by(type=recitation_type)

        if date_only:
            query = query.filter(cast(recitation_session.date, Date) == date_only)
        else:
            if start_date:
                query = query.filter(recitation_session.date >= start_date)
            if end_date:
                query = query.filter(recitation_session.date <= end_date)

        query = (query
            .join(StartVerse, StartVerse.verse_id == recitation_session.start_verse_id)
            .join(StartSurah, StartSurah.surah_id == StartVerse.surah_id)
            .join(EndVerse, EndVerse.verse_id == recitation_session.end_verse_id)
            .join(EndSurah, EndSurah.surah_id == EndVerse.surah_id)
            .add_columns(
                recitation_session,
                StartVerse.order_in_surah.label('start_verse_order'),
                StartSurah.name.label('start_surah_name'),
                EndVerse.order_in_surah.label('end_verse_order'),
                EndSurah.name.label('end_surah_name')
            )
            .order_by(recitation_session.date.desc())
        )

        if limit_count:
            query = query.limit(limit_count)

        return query.all()

    @staticmethod
    def update_session(session_id, data):
        try:
            new_session = recitation_session.query.get_or_404(session_id)
            if 'is_accepted' in data:
                new_session.is_accepted = data['is_accepted']
            if 'rating' in data:
                new_session.rating = data['rating']
            if 'pages_count' in data:
                new_session.pages_count = data['pages_count']
            if 'fromVerse' in data:
                new_session.start_verse_id = data['fromVerse']
            if 'toVerse' in data:
                new_session.end_verse_id = data['toVerse']
                
            db.session.commit()
            return new_session
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error updating session: {str(e)}")

    @staticmethod
    def delete_session(session_id):
        try:
            session = recitation_session.query.get_or_404(session_id)
            db.session.delete(session)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error deleting session: {str(e)}")


    @staticmethod
    def get_student_sessions_count(student_id, recitation_type=None, start_date=None, end_date=None, date_only=None, is_accepted=None, is_accepted_not_none=None, is_rating_not_none=None):
        query = db.session.query(func.count(recitation_session.session_id))\
            .filter_by(student_id=student_id)

        if is_accepted is not None:
            query = query.filter_by(is_accepted=is_accepted)
        elif is_accepted_not_none:
            query = query.filter(recitation_session.is_accepted.isnot(None))
        elif is_accepted_not_none is False:
            query = query.filter(recitation_session.is_accepted.is_(None))

        if is_rating_not_none:
            query = query.filter(recitation_session.rating.isnot(None))

        if recitation_type:
            query = query.filter_by(type=recitation_type)

        if date_only:
            query = query.filter(cast(recitation_session.date, Date) == date_only)
        else:
            if start_date:
                query = query.filter(recitation_session.date >= start_date)
            if end_date:
                query = query.filter(recitation_session.date <= end_date)

        return query.scalar()
    @staticmethod
    def _get_verse_id(surah_id, verse_order):
        verse = verses.query.filter_by(surah_id=surah_id, order_in_surah=verse_order).first()
        return verse.verse_id if verse else None

    @staticmethod
    def _update_section_rating(student_plan, session, section_data, rating_fields):
        old_rate = session.rating or 0
        new_rate = section_data['grade'] or 0
        
        section_sessions_count = RecitationSessionService.get_student_sessions_count(
            student_id=student_plan.student_id,
            recitation_type=session.type,
            is_rating_not_none=True
        )
        
        current_rating = getattr(student_plan, rating_fields[session.type]) or 0
        sum_old_section_rating = (current_rating * section_sessions_count) - old_rate + new_rate
        
        if not session.rating:
            section_sessions_count += 1
            
        return {
            'new_rate': new_rate,
            'old_rate': old_rate,
            'rating_value': sum_old_section_rating / (section_sessions_count * 1.0)
        }

    @staticmethod
    def _prepare_session_update(section_data):
        update_data = {
            'is_accepted': section_data['is_accepted'],
            'rating': section_data['grade']
        }
        
        from_verse_id = RecitationSessionService._get_verse_id(
            section_data['fromSurah'],
            section_data['fromVerse']
        )
        to_verse_id = RecitationSessionService._get_verse_id(
            section_data['toSurah'],
            section_data['toVerse']
        )
        
        if from_verse_id:
            update_data['fromVerse'] = from_verse_id
        if to_verse_id:
            update_data['toVerse'] = to_verse_id
            
        return update_data

    @staticmethod
    def process_sessions_and_eval(student_id, data):
        try:            
            student_plan = StudentPlanInfoService.get_planInfo(student_id)
            if not student_plan:
                raise Exception('Student plan not found')

            rating_fields = {
                'New_Memorization': 'overall_rating_new_memorization',
                'Major_Revision': 'overall_rating_large_revision',
                'Minor_Revision': 'overall_rating_small_revision'
            }

            # Initialize overall rating calculation
            sessions_count = RecitationSessionService.get_student_sessions_count(student_id, is_rating_not_none=True)
            sum_old_overall_rating = (student_plan.overall_rating or 0) * sessions_count
            plan_update_data = {}

            # Process each section
            for section_type, section_data in data['sections'].items():
                session = RecitationSessionService.get_session(section_data['session_id'])
                
                # Update section rating
                rating_update = RecitationSessionService._update_section_rating(
                    student_plan, session, section_data, rating_fields
                )
                sum_old_overall_rating += rating_update['new_rate'] - rating_update['old_rate']
                plan_update_data[rating_fields[session.type]] = rating_update['rating_value']

                # Update session data
                update_data = RecitationSessionService._prepare_session_update(section_data)
                RecitationSessionService.update_session(session.session_id, update_data)

                # Update last verse if accepted
                if section_data['is_accepted']:
                    if session.type == 'New_Memorization':
                        plan_update_data['last_verse_recited_new_memorization'] = session.end_verse_id
                    elif session.type == 'Major_Revision':
                        plan_update_data['last_verse_recited_large_revision'] = session.end_verse_id

            # Update overall rating
            new_sessions_count = RecitationSessionService.get_student_sessions_count(student_id, is_rating_not_none=True)
            plan_update_data['overall_rating'] = sum_old_overall_rating / new_sessions_count

            # Save updates
            if plan_update_data:
                StudentPlanInfoService.update_planInfo(student_id, plan_update_data)
            
            return True
        except Exception as e:
            raise e