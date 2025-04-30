from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models import students_plans_info as StudentsPlansInfo
from app.models import verses as Verse
from app.models import db
from app.Services.recitation_session_Service import RecitationSessionService
from datetime import date, timedelta

class PlanGenerationService:
    def __init__(self):
        self.db = db

    def generate_plan(self, student_id, start_date=date.today(), isUpdate=False):
        try:
            # fake_date = "2025-03-02"  #! I transferred it to Students_Services line 36
            # start_date = date.fromisoformat(fake_date) if fake_date else date.today()
            plan_data = self._initialize_plan_data(student_id, start_date)
            
            for day in plan_data['days']:
                current_date = date.fromisoformat(day["date"])
                self._generate_daily_plan(
                    student_id=student_id,
                    current_date=current_date,
                    memo_data=plan_data['memo'],
                    minor_rev_data=plan_data['minor_rev'],
                    major_rev_data=plan_data['major_rev'], 
                    isUpdate=isUpdate
                )
                #Update
                plan_data['minor_rev']['memo_sissions'] = self._get_past_memo_sessions(student_id, current_date)
        except Exception as e:
            self.db.session.rollback()
            raise RuntimeError(f"Plan generation failed: {str(e)}")

    def _initialize_plan_data(self, student_id, start_date):
        plan_info = self.get_student_plan(student_id)
        days_info = self.get_memorization_days_info(plan_info.memorization_days, start_date=start_date)
        mem_sissions = RecitationSessionService.get_student_sessions(student_id=student_id, recitation_type='New_Memorization', ascending=False, is_accepted=True, end_date=start_date - timedelta(days=1))
        
        return {
            'days': days_info["days"],
            'memo': {
                'last_verse': plan_info.last_verse_recited_new_memorization,
                'letters_amount': plan_info.new_memorization_letters_amount,
                'pages_amount': plan_info.new_memorization_pages_amount,
                'direction': plan_info.memorization_direction
            },
            'minor_rev': {
                'letters_amount': plan_info.small_revision_letters_amount,
                'pages_amount': plan_info.small_revision_pages_amount,
                'memo_sissions': self._get_past_memo_sessions(student_id, start_date, isFirstDayWeek=True)
            },
            'major_rev': {
                'last_verse': plan_info.last_verse_recited_large_revision,
                'letters_amount': plan_info.large_revision_letters_amount,
                'pages_amount': plan_info.large_revision_pages_amount,
                'direction': plan_info.revision_direction
            }
        }

    def get_student_plan(self, student_id):
        """Helper method to get student plan info"""
        plan_info = self.db.session.query(StudentsPlansInfo).filter(
            StudentsPlansInfo.student_id == student_id
        ).first()
        if not plan_info:
            raise ValueError("Student plan info not found")
        return plan_info

    def _generate_daily_plan(self, student_id, current_date, memo_data, minor_rev_data, major_rev_data, isUpdate=False):
        memo_result = self._generate_memorization(student_id, current_date, memo_data, isUpdate)
        minor_rev_result = self._generate_minor_revision(student_id, current_date, minor_rev_data, isUpdate)
        self._generate_major_revision(student_id, current_date, major_rev_data, minor_rev_result, memo_result, memo_data, isUpdate)

    def _generate_minor_revision(self, student_id, current_date, minor_rev_data, isUpdate=False):
        if minor_rev_data['letters_amount']:
            minor_revision_plan = self.generate_minor_revision_plan(student_id, minor_rev_data['letters_amount'], minor_rev_data['memo_sissions'])
        elif minor_rev_data['pages_amount']:
            minor_revision_plan = self.generate_minor_revision_plan(student_id, minor_rev_data['pages_amount'], minor_rev_data['memo_sissions'], amount_type='pages')
        else:
            minor_revision_plan = self.generate_minor_revision_plan(student_id, 1, minor_rev_data['memo_sissions'], amount_type='default')
        
        if minor_revision_plan:
            self.store_plan_in_database(student_id, minor_revision_plan, 'Minor_Revision', current_date, isUpdate)
            return {
                'current_surah': self.get_current_surah(minor_revision_plan['start_verse_id'])
            }
        return None

    def _generate_memorization(self, student_id, current_date, memo_data, isUpdate=False):
        memo_start_verse = self.get_start_verse(memo_data['last_verse'], memo_data['direction'])
        if not memo_start_verse:
            return None

        if memo_data['letters_amount']:
            memo_plan = self.generate_plan_by_amount(memo_start_verse, memo_data['letters_amount'], memo_data['direction'])
        elif memo_data['pages_amount']:
            memo_plan = self.generate_plan_by_amount(memo_start_verse, memo_data['pages_amount'], memo_data['direction'], amount_type='pages')
        else:
            memo_plan = self.generate_plan_by_difficulty(memo_start_verse, memo_data['direction'])
        
        if memo_plan:
            self.store_plan_in_database(student_id, memo_plan, 'New_Memorization', current_date, isUpdate)
            memo_data['last_verse'] = memo_plan['end_verse_id']
            return {
                'current_surah': self.get_current_surah(memo_plan['start_verse_id'])
            }
        return None

    def _generate_major_revision(self, student_id, current_date, major_rev_data, minor_rev_result, memo_result, memo_data, isUpdate=False):
        majorRev_start_verse = self.get_start_verse(major_rev_data['last_verse'], major_rev_data['direction']) if major_rev_data['last_verse'] else None
        current_surah = 0

        if minor_rev_result and minor_rev_result['current_surah']:
            if not majorRev_start_verse or majorRev_start_verse.surah_id == minor_rev_result['current_surah']:
                majorRev_start_verse = self.update_majorRev_start_verse(minor_rev_result['current_surah'], major_rev_data['direction'], memo_data['direction'])
                current_surah = minor_rev_result['current_surah']
        elif memo_result and memo_result['current_surah']:
            if not majorRev_start_verse or majorRev_start_verse.surah_id == memo_result['current_surah']:
                majorRev_start_verse = self.update_majorRev_start_verse(memo_result['current_surah'], major_rev_data['direction'], memo_data['direction'])
                current_surah = memo_result['current_surah']

        if majorRev_start_verse:
            if major_rev_data['letters_amount']:
                majorRev_plan = self.generate_plan_by_amount(majorRev_start_verse, major_rev_data['letters_amount'], major_rev_data['direction'], stop_place=current_surah)
            elif major_rev_data['pages_amount']:
                majorRev_plan = self.generate_plan_by_amount(majorRev_start_verse, major_rev_data['pages_amount'], major_rev_data['direction'], amount_type='pages', stop_place=current_surah)
            else:
                majorRev_plan = self.generate_plan_by_difficulty(majorRev_start_verse, major_rev_data['direction'], factor=10)
            
            if majorRev_plan:
                self.store_plan_in_database(student_id, majorRev_plan, 'Major_Revision', current_date, isUpdate)
                major_rev_data['last_verse'] = majorRev_plan['end_verse_id']
        
    def generate_plan_by_amount(self, start_verse, required_amount, direction, amount_type='letters', stop_place=0):
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

                if not next_verse or next_verse.surah_id == stop_place:
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

            if remaining_verses:
                remaining_amount = sum(getattr(v, amount_attr) for v in remaining_verses)
                if (total_plan_amount + remaining_amount) <= (required_amount * 1.10):
                    verses_in_plan.extend(remaining_verses)
                    total_plan_amount += remaining_amount
                    end_verse = remaining_verses[-1] if remaining_verses else end_verse

            return self.format_plan_response(start_verse.verse_id, end_verse.verse_id, total_letters, total_pages)

        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Plan generation failed: {str(e)}")

    def generate_plan_by_difficulty(self, start_verse, direction, factor=1):
        try:
            total_difficulty = 0
            total_plan_letters = 0
            total_pages = 0
            current_verse = start_verse
            end_verse = start_verse
            current_surah = start_verse.surah_id
            index_column = Verse.order_in_quraan if direction else Verse.reverse_index
            verses_in_plan = []

            while total_difficulty < factor:
                
                potential_total = total_difficulty + current_verse.verse_difficulty
                
                if potential_total > factor:
                    diff_with = abs(potential_total - factor)
                    diff_without = abs(factor - total_difficulty)
                    if diff_without < diff_with:
                        break
                
                verses_in_plan.append(current_verse)
                total_difficulty += current_verse.verse_difficulty
                total_plan_letters += current_verse.letters_count
                total_pages += current_verse.weight_on_page
                end_verse = current_verse
                
                current_index = getattr(current_verse, index_column.key)
                next_verse = db.session.query(Verse).filter(
                    index_column == current_index + 1
                ).first()

                if not next_verse:
                    break

                if next_verse.surah_id != current_surah:
                    remaining_allowance = factor - total_difficulty
                    if remaining_allowance < (factor * 0.10):
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
            if (total_difficulty + remaining_difficulty) <= (factor * 0.10):
                verses_in_plan.extend(remaining_verses)
                total_difficulty += remaining_difficulty
                end_verse = remaining_verses[-1] if remaining_verses else end_verse
    
            return self.format_plan_response(start_verse.verse_id, end_verse.verse_id, total_plan_letters, total_pages)

        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Plan generation failed: {str(e)}")

    def generate_minor_revision_plan(self, student_id, required_amount, new_memo_sessions, amount_type='letters'):
        try:
            
            if not new_memo_sessions:
                return None
            
            # new_memo_sessions = [s[0] for s in sessions]
            new_memo_sessions = [self.db.session.merge(session) for session in new_memo_sessions]

            if amount_type == 'default':
                included_sessions = new_memo_sessions[:3]
                if included_sessions:
                    total_letters = sum(s.letters_count for s in included_sessions)
                    total_pages = sum(s.pages_count for s in included_sessions)
                    start_verse = included_sessions[-1].start_verse_id
                    end_verse = included_sessions[0].end_verse_id
                    return self.format_plan_response(start_verse, end_verse, total_letters, total_pages)
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

    def store_plan_in_database(self, student_id, plan_data, recitation_type, plan_date=None, isUpdate=False):
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
            if isUpdate:
                old_session = RecitationSessionService.get_student_sessions(student_id=student_id, recitation_type=recitation_type, date_only=plan_date)[0][0]
                return RecitationSessionService.update_session(old_session.session_id, session_data)
            return RecitationSessionService.create_session(session_data)
        except Exception as e:
            self.db.session.rollback()
            raise RuntimeError(f"Failed to store plan in database: {str(e)}")

    # Helper methods
    def get_start_verse(self, last_verse, direction):
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

    def get_current_surah(self, temp_verse):
        current_verse = self.db.session.query(Verse).filter(
            Verse.verse_id == temp_verse
            ).first()

        current_surah = current_verse.surah_id

        return current_surah

    def update_majorRev_start_verse(self, temp_surah, majorRev_direction, memo_direction):        
        if memo_direction:
            if majorRev_direction:
                current_surah = 1 if temp_surah != 1 else 0
            else:
                current_surah = temp_surah - 1
        else:
            if majorRev_direction:
                current_surah = temp_surah + 1
            else:
                current_surah = 114 if temp_surah != 114 else 0

        if current_surah < 1 or current_surah > 114:
            return None

        majorRev_start_verse = self.db.session.query(Verse).filter(
            and_(
                Verse.surah_id == current_surah,
                Verse.order_in_surah == 1
            )
        ).first()
        
        return majorRev_start_verse

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

    def _get_past_memo_sessions(self, student_id, current_date, isFirstDayWeek=False): 
        try:
            if isFirstDayWeek:
                sessions = RecitationSessionService.get_student_sessions(student_id=student_id, recitation_type='New_Memorization', ascending=False, is_accepted=True, end_date=current_date - timedelta(days=1))
            else:
                sessions = RecitationSessionService.get_student_sessions(student_id=student_id, recitation_type='New_Memorization', ascending=False, is_accepted=True, is_accepted_not_none=False, end_date=current_date)
            if not sessions:
                return None
            return [s[0] for s in sessions]

        except Exception as e:
            raise RuntimeError(f"Failed to get past memorization sessions: {str(e)}")
