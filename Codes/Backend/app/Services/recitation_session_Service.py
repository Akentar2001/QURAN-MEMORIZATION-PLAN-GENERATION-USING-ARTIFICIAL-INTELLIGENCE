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
    def get_student_sessions(student_id, recitation_type=None, limit_count=None, start_date=None, end_date=None, date_only=None, is_accepted=None, is_accepted_not_none=None, is_rating_not_none=None, after_session=None, ascending=False):
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

        if after_session:
            query = query.filter(recitation_session.session_id > after_session)

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
            .order_by(recitation_session.session_id if ascending else recitation_session.session_id.desc())
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