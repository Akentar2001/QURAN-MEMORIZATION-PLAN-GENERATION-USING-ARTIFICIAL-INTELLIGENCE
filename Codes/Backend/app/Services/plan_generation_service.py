from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models import students_plans_info as StudentsPlansInfo
from app.models import verses as Verse
from app.models import db
from app.Services.recitation_session_Service import RecitationSessionService
from datetime import date

class PlanGenerationService:
    def __init__(self):
        self.db = db

    def generate_plan(self, student_id):
        try:
            plan_info = self.get_student_plan(student_id)
            test_date = "2025-04-13"
            days_info = self.get_memorization_days_info(plan_info.memorization_days, test_date)
            days = days_info["days"]

            last_verse = plan_info.last_verse_recited_new_memorization
            required_memo_letters_amount = plan_info.new_memorization_letters_amount
            required_memo_pages_amount = plan_info.new_memorization_pages_amount
            direction = plan_info.memorization_direction

            required_minorRev_letters_amount = plan_info.small_revision_letters_amount
            required_minorRev_pages_amount = plan_info.small_revision_pages_amount

            for day in days:
                current_date = day["date"]
                if required_minorRev_letters_amount:
                    minor_revision_plan = self.generate_minor_revision_plan(student_id, required_minorRev_letters_amount)
                elif required_minorRev_pages_amount:
                    minor_revision_plan = self.generate_minor_revision_plan(student_id, required_minorRev_pages_amount, amount_type='pages')
                
                if minor_revision_plan:
                    self.store_plan_in_database(student_id, minor_revision_plan, 'Minor_Revision', current_date)


                start_verse = self.get_start_verse(last_verse, direction)
                if start_verse:
                    if required_memo_letters_amount:
                        memo_plan = self.generate_memorization_plan(start_verse, required_memo_letters_amount, direction)
                    elif required_memo_pages_amount:
                        memo_plan = self.generate_memorization_plan(start_verse, required_memo_pages_amount, direction, amount_type='pages')
                    else:
                        memo_plan = self.generate_memorization_plan_using_difficulty(start_verse, direction)
                    
                    if memo_plan:
                        self.store_plan_in_database(student_id, memo_plan, 'New_Memorization', current_date)
                        last_verse = memo_plan['end_verse_id']
            
        except Exception as e:
            self.db.session.rollback()
            raise RuntimeError(f"Plan generation failed: {str(e)}")


    def get_student_plan(self, student_id):
        """Helper method to get student plan info"""
        plan_info = self.db.session.query(StudentsPlansInfo).filter(
            StudentsPlansInfo.student_id == student_id
        ).first()
        if not plan_info:
            raise ValueError("Student plan info not found")
        return plan_info

    def get_start_verse(self, last_verse, direction):
        """Helper method to determine starting verse"""
        index_column = Verse.order_in_quraan if direction else Verse.reverse_index

        start_verse = self.db.session.query(Verse).filter(
            Verse.verse_id == last_verse
        ).first()

        if not start_verse:
            start_verse = self.db.session.query(Verse).order_by(index_column.asc()).first()
        else:
            current_index = getattr(start_verse, index_column.key)
            next_verse = self.db.session.query(Verse).filter(
                index_column == current_index + 1
            ).first()

            if next_verse:
                start_verse = next_verse
            else:
                return None

        if not start_verse:
            raise ValueError("No verses found in database")
            
        return start_verse

        
    def generate_memorization_plan(self, start_verse, required_amount, direction, amount_type='letters'):
        try:
            total_plan_amount = 0
            total_letters = 0
            total_pages = 0
            current_verse = start_verse
            end_verse = start_verse
            current_surah = start_verse.surah_id
            index_column = Verse.order_in_quraan if direction else Verse.reverse_index
            amount_attr = 'letters_count' if amount_type == 'letters' else 'weight_on_page'
            verses_in_plan = []
            while total_plan_amount <= required_amount:
                current_amount = getattr(current_verse, amount_attr)
                potential_total = total_plan_amount + current_amount
                
                if potential_total > required_amount:
                    diff_with = abs(potential_total - required_amount)
                    diff_without = abs(required_amount - total_plan_amount)
                    if diff_without < diff_with:
                        break
                
                verses_in_plan.append(current_verse)
                total_plan_amount += current_amount
                total_letters += current_verse.letters_count
                total_pages += current_verse.weight_on_page
                end_verse = current_verse
                
                current_index = getattr(current_verse, index_column.key)
                next_verse = db.session.query(Verse).filter(
                    index_column == current_index + 1
                ).first()

                if not next_verse:
                    break

                if next_verse.surah_id != current_surah:
                    remaining_allowance = required_amount - total_plan_amount
                    if remaining_allowance < (required_amount * 0.10):
                        break
                    current_surah = next_verse.surah_id

                current_verse = next_verse

            remaining_verses = db.session.query(Verse).filter(
                and_(
                    Verse.surah_id == current_surah,
                    index_column > getattr(end_verse, index_column.key)
                )
            ).order_by(index_column.asc()).all()

            remaining_amount = sum(getattr(v, amount_attr) for v in remaining_verses)
            if (total_plan_amount + remaining_amount) <= (required_amount * 1.10):
                verses_in_plan.extend(remaining_verses)
                total_plan_amount += remaining_amount
                end_verse = remaining_verses[-1] if remaining_verses else end_verse

            return self.format_plan_response(start_verse.verse_id, end_verse.verse_id, total_letters, total_pages)

        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Plan generation failed: {str(e)}")

    def generate_minor_revision_plan(self, student_id, required_amount, amount_type='letters'):
        try:
            sessions = RecitationSessionService.get_student_sessions(student_id, 'New_Memorization')
            
            new_memo_sessions = sorted([s[0] for s in sessions], 
                                    key=lambda x: x.created_at, 
                                    reverse=True)
            
            if not new_memo_sessions:
                return None

            latest_session = new_memo_sessions[0]
            total_plan_amount = latest_session.letters_count if amount_type == 'letters' else latest_session.pages_count
            total_letters = latest_session.letters_count
            total_pages = latest_session.pages_count
            current_start_verse = latest_session.start_verse_id
            included_sessions = [latest_session]

            for session in new_memo_sessions[1:]:
                current_amount = session.letters_count if amount_type == 'letters' else session.pages_count
                potential_total = total_plan_amount + current_amount
                
                diff_with = abs(potential_total - required_amount)
                diff_without = abs(required_amount - total_plan_amount)
                
                if diff_without < diff_with:
                    break
                
                included_sessions.append(session)
                total_plan_amount = potential_total
                total_letters += session.letters_count
                total_pages += session.pages_count
                current_start_verse = session.start_verse_id
            
            if included_sessions:
                start_verse = current_start_verse
                end_verse = latest_session.end_verse_id
                return self.format_plan_response(start_verse, end_verse, total_letters, total_pages)
                
            return None
            
        except Exception as e:
            self.db.session.rollback()
            raise RuntimeError(f"Minor revision plan generation failed: {str(e)}")

    def format_plan_response(self, start_verse, end_verse, total_letters, total_pages):
        return {
            "start_verse_id": start_verse,
            "end_verse_id": end_verse,
            "total_letters": total_letters,
            "total_pages": total_pages,
        }

    def store_plan_in_database(self, student_id, plan_data, recitation_type, plan_date=None):
        try:
            session_data = {
                'student_id': student_id,
                'type': recitation_type,
                'start_verse_id': plan_data['start_verse_id'],
                'end_verse_id': plan_data['end_verse_id'],
                'letters_count': plan_data['total_letters'],
                'pages_count': plan_data['total_pages'],
                'date': plan_date if plan_date else date.today()
            }
            
            return RecitationSessionService.create_session(session_data)
        except Exception as e:
            self.db.session.rollback()
            raise RuntimeError(f"Failed to store plan in database: {str(e)}")

    def generate_memorization_plan_using_difficulty(self, start_verse, direction):
        try:
            total_difficulty = 0
            total_plan_letters = 0
            current_verse = start_verse
            end_verse = start_verse
            current_surah = start_verse.surah_id
            index_column = Verse.order_in_quraan if direction else Verse.reverse_index
            verses_in_plan = []

            while total_difficulty < 1:
                
                potential_total = total_difficulty + current_verse.verse_difficulty
                
                if potential_total > 1:
                    diff_with = abs(potential_total - 1)
                    diff_without = abs(1 - total_difficulty)
                    if diff_without < diff_with:
                        break
                
                verses_in_plan.append(current_verse)
                total_difficulty += current_verse.verse_difficulty
                total_plan_letters += current_verse.letters_count
                end_verse = current_verse
                
                current_index = getattr(current_verse, index_column.key)
                next_verse = db.session.query(Verse).filter(
                    index_column == current_index + 1
                ).first()

                if not next_verse:
                    break

                if next_verse.surah_id != current_surah:
                    remaining_allowance = 1 - total_difficulty
                    if remaining_allowance < 0.10:
                        break
                    current_surah = next_verse.surah_id

                current_verse = next_verse

            remaining_verses = db.session.query(Verse).filter(
                and_(
                    Verse.surah_id == current_surah,
                    index_column > getattr(end_verse, index_column.key)
                )
            ).order_by(index_column.asc()).all()

            remaining_difficulty = sum(v.verse_difficulty for v in remaining_verses)
            if (total_difficulty + remaining_difficulty) <= 1.10:
                verses_in_plan.extend(remaining_verses)
                total_difficulty += remaining_difficulty
                end_verse = remaining_verses[-1] if remaining_verses else end_verse

            return self.format_plan_response(start_verse, end_verse, total_plan_letters, verses_in_plan)

        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Plan generation failed: {str(e)}")

    def get_memorization_days_info(self, memorization_days, start_date=None):
        """Helper method to get information about memorization days"""
        from datetime import datetime, timedelta

        if start_date is None:
            start_date = datetime.now()
        elif isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')

        week_days = [
            {"name": "الأحد", "name_en": "Sunday", "value": 1},
            {"name": "الاثنين", "name_en": "Monday", "value": 2},
            {"name": "الثلاثاء", "name_en": "Tuesday", "value": 4},
            {"name": "الأربعاء", "name_en": "Wednesday", "value": 8},
            {"name": "الخميس", "name_en": "Thursday", "value": 16},
            {"name": "الجمعة", "name_en": "Friday", "value": 32},
            {"name": "السبت", "name_en": "Saturday", "value": 64}
        ]

        # Get current day index (0 = Monday, 6 = Sunday)
        current_day_index = start_date.weekday()
        # Convert to Sunday = 0 format
        current_day_index = (current_day_index + 1) % 7

        # Calculate remaining days
        remaining_days = []
        total_value = 0

        for i in range(current_day_index, 7):
            day = week_days[i]
            if memorization_days & day["value"]:
                day_date = start_date + timedelta(days=(i - current_day_index))
                remaining_days.append({
                    "name": day["name"],
                    "name_en": day["name_en"],
                    "value": day["value"],
                    "date": day_date.strftime('%Y-%m-%d')
                })
                total_value += day["value"]
        
        return {
            "days": remaining_days,
            "count": len(remaining_days),
            "names": [day["name"] for day in remaining_days],
            "names_en": [day["name_en"] for day in remaining_days],
            "dates": [day["date"] for day in remaining_days],
            "total_value": total_value
        }