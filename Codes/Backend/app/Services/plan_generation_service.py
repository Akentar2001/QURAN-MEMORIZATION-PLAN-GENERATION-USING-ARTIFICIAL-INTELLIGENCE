from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models import students_plans_info as StudentsPlansInfo
from app.models import verses as Verse
from app.models import db
from app.Services.recitation_session_Service import RecitationSessionService

class PlanGenerationService:
    def __init__(self):
        self.db = db

    def generate_plan(self, student_id):
        try:
            plan_info = self.get_student_plan(student_id)
            last_verse = plan_info.last_verse_recited
            days_info = self.get_memorization_days_info(plan_info.memorization_days)
            days = days_info["days"]
            required_amount = plan_info.new_memorization_amount
            direction = plan_info.memorization_direction

            for day in days:
                start_verse = self.get_start_verse(last_verse, direction)
                if start_verse:
                    if required_amount:
                        plan = self.generate_memorization_plan(start_verse, required_amount, direction)
                    else:
                        plan = self.generate_memorization_plan_using_difficulty(start_verse, direction)
                    
                    if not plan:
                        break

                    self.store_plan_in_database(student_id, plan, 'New_Memorization')
                    last_verse = plan['end_verse_id']
            
        except Exception as e:
            self.db.session.rollback()
            raise RuntimeError(f"Plan generation failed: {str(e)}")

            # if recitation_type == "new_memorization":
            #     return self.generate_memorization_plan(start_verse, plan_info)
            # elif recitation_type == "minor_revision":
            #     return self.generate_minor_revision_plan(start_verse, plan_info)
            # elif recitation_type == "major_revision":
            #     return self.generate_major_revision_plan(start_verse, plan_info)
            # else:
            #     raise ValueError("Invalid recitation type")


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

        
    def generate_memorization_plan(self, start_verse, required_amount, direction):
        try:
            total_plan_letters = 0
            current_verse = start_verse
            end_verse = start_verse
            current_surah = start_verse.surah_id
            index_column = Verse.order_in_quraan if direction else Verse.reverse_index
            verses_in_plan = []

            while total_plan_letters < required_amount:
                
                potential_total = total_plan_letters + current_verse.letters_count
                
                if potential_total > required_amount:
                    diff_with = abs(potential_total - required_amount)
                    diff_without = abs(required_amount - total_plan_letters)
                    if diff_without < diff_with:
                        break
                
                verses_in_plan.append(current_verse)
                total_plan_letters += current_verse.letters_count
                end_verse = current_verse
                
                current_index = getattr(current_verse, index_column.key)
                next_verse = db.session.query(Verse).filter(
                    index_column == current_index + 1
                ).first()

                if not next_verse:
                    break

                if next_verse.surah_id != current_surah:
                    remaining_allowance = required_amount - total_plan_letters
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

            remaining_letters = sum(v.letters_count for v in remaining_verses)
            if (total_plan_letters + remaining_letters) <= (required_amount * 1.10):
                verses_in_plan.extend(remaining_verses)
                total_plan_letters += remaining_letters
                end_verse = remaining_verses[-1] if remaining_verses else end_verse

            return self.format_plan_response(start_verse, end_verse, total_plan_letters, verses_in_plan)

        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Plan generation failed: {str(e)}")


    def format_plan_response(self, start_verse, end_verse, total_letters, verses_in_plan):

        return {
            "start_verse_id": start_verse.verse_id,
            "end_verse_id": end_verse.verse_id,
            "total_letters": total_letters,
            "verses_count": len(verses_in_plan),
            "surahs_count": len({v.surah_id for v in verses_in_plan})
        }

    def store_plan_in_database(self, student_id, plan_data, recitation_type):
        try:
            if 'start_verse_id' in plan_data:
                session_data = {
                    'student_id': student_id,
                    'type': recitation_type,
                    'start_verse_id': plan_data['start_verse_id'],
                    'end_verse_id': plan_data['end_verse_id'],
                    'letters_count': plan_data['total_letters']
                }
                
                return RecitationSessionService.create_session(session_data)
            return None
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

    def get_memorization_days_info(self, memorization_days):
        """Helper method to get information about memorization days"""
        week_days = [
            {"name": "الأحد", "value": 1},
            {"name": "الاثنين", "value": 2},
            {"name": "الثلاثاء", "value": 4},
            {"name": "الأربعاء", "value": 8},
            {"name": "الخميس", "value": 16},
            {"name": "الجمعة", "value": 32},
            {"name": "السبت", "value": 64}
        ]
        
        active_days = []
        for day in week_days:
            if memorization_days & day["value"]:
                active_days.append(day)
        
        return {
            "days": active_days,
            "count": len(active_days),
            "names": [day["name"] for day in active_days]
        }