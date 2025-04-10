from datetime import date
from app.models import db, recitation_session, verses, surahs
from sqlalchemy.orm import aliased

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
            if 'rl_reward_signal' in data:
                new_session.rl_reward_signal = data['rl_reward_signal']
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
    def get_student_sessions(student_id, recitation_type=None):
        StartVerse = aliased(verses)
        EndVerse = aliased(verses)
        StartSurah = aliased(surahs)
        EndSurah = aliased(surahs)

        query = (recitation_session.query
            .filter_by(student_id=student_id))
            
        if recitation_type:
            query = query.filter_by(type=recitation_type)
            
        return (query
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
            .all())

    @staticmethod
    def update_session(session_id, data):
        try:
            new_session = recitation_session.query.get_or_404(session_id)
            
            if 'is_accepted' in data:
                new_session.is_accepted = data['is_accepted']
            if 'rating' in data:
                new_session.rating = data['rating']
            if 'rl_reward_signal' in data:
                new_session.rl_reward_signal = data['rl_reward_signal']
            if 'pages_count' in data:
                new_session.pages_count = data['pages_count']
                
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