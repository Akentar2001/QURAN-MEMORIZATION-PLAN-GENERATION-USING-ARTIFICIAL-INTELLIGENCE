from app import db
from app.models import students_plans_info, verses
from datetime import datetime

class StudentPlanInfoService:
    @staticmethod
    def create_planInfo(student_id, data):

        verse = verses.query.filter_by(surah_id=data['start_surah'], order_in_surah=data['no_verse_in_surah']).first()
        rev_verse = verses.query.filter_by(surah_id=data['rev_from_surah'], order_in_surah=data['rev_from_verse']).first()
        last_verse_memo = StudentPlanInfoService.calculate_last_verse_recited(verse, data['memorization_direction'])
        last_verse_rev = StudentPlanInfoService.calculate_last_verse_recited(rev_verse, data['revision_direction'])

        student_plan = students_plans_info(
            student_id=student_id,
            memorization_direction=data.get('memorization_direction'),
            revision_direction=data.get('revision_direction'),
            memorization_days=data.get('memorization_days', 5),
            last_verse_recited_new_memorization=last_verse_memo,
            last_verse_recited_large_revision=last_verse_rev if last_verse_rev else None
            )

        student_plan.memorized_parts = StudentPlanInfoService.calculate_memorized_parts(student_plan.last_verse_recited_new_memorization, student_plan.memorization_direction)

        optional_fields = [
            'overall_rating',
            'new_memorization_letters_amount',
            'new_memorization_pages_amount',
            'small_revision_letters_amount',
            'small_revision_pages_amount',
            'large_revision_letters_amount',
            'large_revision_pages_amount',
            'last_verse_recited_large_revision',
            'overall_rating_new_memorization',
            'overall_rating_large_revision',
            'overall_rating_small_revision',
            'rl_last_action'
        ]
        
        for field in optional_fields:
            if field in data:
                setattr(student_plan, field, data[field])

        student_plan.created_at = datetime.utcnow()
        student_plan.updated_at = datetime.utcnow()

        db.session.add(student_plan)
        db.session.commit()
        db.session.flush()
        
        return student_plan

    @staticmethod
    @staticmethod
    def get_planInfo(student_id):
        try:
            plan_info = students_plans_info.query.get(student_id)
        except Exception as e:
            print(f"Error querying students_plans_info: {e}")
            raise
            
        if plan_info:
            StudentPlanInfoService.calculate_start_surah_and_verse(plan_info)
    
        return plan_info

    @staticmethod
    def update_planInfo(student_id, plan_data):
        plan_info = students_plans_info.query.get(student_id)
        
        if plan_info:
            if 'memorization_direction' in plan_data:
                plan_info.memorization_direction = plan_data['memorization_direction']
            if 'revision_direction' in plan_data:
                plan_info.revision_direction = plan_data['revision_direction']
            if 'memorization_days' in plan_data:
                plan_info.memorization_days = plan_data['memorization_days']
            if 'last_verse_recited_new_memorization' in plan_data:
                plan_info.last_verse_recited_new_memorization = plan_data['last_verse_recited_new_memorization']
            if 'last_verse_recited_large_revision' in plan_data:
                plan_info.last_verse_recited_large_revision = plan_data['last_verse_recited_large_revision']
            if 'start_surah' in plan_data and 'no_verse_in_surah' in plan_data:
                verse = verses.query.filter_by(surah_id=plan_data['start_surah'], order_in_surah=plan_data['no_verse_in_surah']).first()
                last_verse = StudentPlanInfoService.calculate_last_verse_recited(verse, plan_data.get('memorization_direction', plan_info.memorization_direction))
                plan_info.last_verse_recited_new_memorization = last_verse

            optional_fields = [
                'new_memorization_letters_amount',
                'new_memorization_pages_amount',
                'small_revision_letters_amount',
                'small_revision_pages_amount',
                'large_revision_letters_amount',
                'large_revision_pages_amount',
                'last_verse_recited_large_revision',
                'overall_rating',
                'overall_rating_new_memorization',
                'overall_rating_large_revision',
                'overall_rating_small_revision',
                'rl_last_action'
            ]
            
            for field in optional_fields:
                if field in plan_data:
                    setattr(plan_info, field, plan_data[field])

            plan_info.memorized_parts = StudentPlanInfoService.calculate_memorized_parts(
                plan_info.last_verse_recited_new_memorization, 
                plan_info.memorization_direction
            )
            
            # fake_date = "2025-03-02"  #! Change this to the desired start date
            # start_date = date.fromisoformat(fake_date) if fake_date else date.today()

            # plan_generator = PlanGenerationService()
            # plan_generator.generate_plan(new_student.student_id, start_date=start_date)

            plan_info.updated_at = datetime.utcnow()
            db.session.commit()
            
            return plan_info
        return None

    @staticmethod
    def delete_planInfo(student_id):
        plan_info = students_plans_info.query.get(student_id)
        if plan_info:
            db.session.delete(plan_info)
            db.session.commit()
            return True
        return False

    @staticmethod
    def calculate_memorized_parts(last_verse_id, memorization_direction):
        verse = verses.query.get(last_verse_id)
        if not verse:
            return 0.0
        surah_id = verse.surah_id
        current_page_no = verse.page_no
        if memorization_direction:
            memorized_parts = current_page_no / 20
        else:
            first_page_query = verses.query.filter_by(surah_id=surah_id).order_by(verses.verse_id.asc()).first()
            if not first_page_query:
                return 0.0
            first_page_of_current_surah = first_page_query.page_no
            
            next_surah_query = verses.query.filter_by(surah_id=(surah_id + 1)).order_by(verses.verse_id.asc()).first()
            if not next_surah_query:
                memorized_parts = 0.01
            else:
                first_page_of_next_surah = next_surah_query.page_no
                memorized_parts = ((602 - first_page_of_next_surah) + (current_page_no - first_page_of_current_surah + 1)) / 20
            
        if memorized_parts < 0:
            memorized_parts = 0.05

        if memorized_parts > 30:
            memorized_parts = 30

        return memorized_parts

    @staticmethod
    def calculate_last_verse_recited(verse, memorization_direction):
        if not verse:
            return 6231
            
        if memorization_direction:
            return verse.verse_id - 1
        
        rev_verse = verses.query.filter_by(reverse_index=verse.reverse_index - 1).first()
        return rev_verse.verse_id if rev_verse else 0

    @staticmethod
    def calculate_start_surah_and_verse(plan_info):
        verse = verses.query.get(plan_info.last_verse_recited_new_memorization)

        if plan_info.memorization_direction:
            if verse:
                next_verse = verses.query.get(plan_info.last_verse_recited_new_memorization + 1)
                if next_verse:
                    plan_info.start_surah = next_verse.surah_id
                    plan_info.no_verse_in_surah = next_verse.order_in_surah
                else:
                    plan_info.start_surah = 1
                    plan_info.no_verse_in_surah = 7
            else:
                plan_info.start_surah = 1
                plan_info.no_verse_in_surah = 1
        else:
            if verse:
                next_verse = verses.query.filter_by(reverse_index=verse.reverse_index + 1).first()
                if next_verse:
                    plan_info.start_surah = next_verse.surah_id
                    plan_info.no_verse_in_surah = next_verse.order_in_surah
                else:
                    plan_info.start_surah = 114
                    plan_info.no_verse_in_surah = 6
            else:
                plan_info.start_surah = 114
                plan_info.no_verse_in_surah = 1