from app.models import students
from app import db
from app.models import students_plans_info
from datetime import datetime
from app.models import verses

class StudentService:
    @staticmethod
    def create_student(data):

        required_fields = ['name', 'age', 'gender', 'nationality']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'Missing required field: {field}')
        new_student = students(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            nationality=data['nationality'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        if 'student_phone' in data:
            new_student.student_phone = data['student_phone']
        if 'parent_phone' in data:
            new_student.parent_phone = data['parent_phone']
        if 'notes' in data:
            new_student.notes = data['notes']
        if 'user_id' in data:
            new_student.user_id = data['user_id']

        db.session.add(new_student)
        db.session.flush() 

        student_plan = students_plans_info(
            student_id = new_student.student_id,
            memorization_direction = data.get('memorization_direction') == "true",
            revision_direction = data.get('revision_direction') == "true"
        )
  
        verse = verses.query.filter_by(surah_id = data['start_surah'], order_in_surah=data['no_verse_in_surah']).first()
        
        student_plan.last_verse_recited = 6231
        if verse:
            if student_plan.memorization_direction:
                student_plan.last_verse_recited = verse.verse_id - 1
            else:
                rev_verse = verses.query.filter_by(reverse_index=verse.reverse_index - 1).first()
                if rev_verse:
                    student_plan.last_verse_recited = rev_verse.verse_id
                else:
                    student_plan.last_verse_recited = 0

        student_plan.memorized_parts = StudentService.calculate_memorized_parts(student_plan.last_verse_recited, student_plan.memorization_direction)
        
        if 'new_memorization_amount' in data:
            student_plan.new_memorization_amount=data['new_memorization_amount']
        if 'small_revision_amount' in data:
            student_plan.small_revision_amount=data['small_revision_amount']
        if 'large_revision_amount' in data:
            student_plan.large_revision_amount=data['large_revision_amount']
        if 'memorization_days' in data:
            student_plan.memorization_days=data['memorization_days']
        
        db.session.add(student_plan)
        db.session.commit()
        return new_student
    
    @staticmethod
    def get_all_students():
        return db.session.query(
            students, 
            students_plans_info
        ).join(
            students_plans_info, 
            students.student_id == students_plans_info.student_id, 
            isouter=True
        ).all()
    
    @staticmethod
    def get_student_by_id(student_id):
        return db.session.query(
            students,
            students_plans_info
        ).join(
            students_plans_info,
            students.student_id == students_plans_info.student_id,
            isouter=True
        ).filter(students.student_id == student_id).first()
    
    @staticmethod
    def update_student(student_id, data):
        student = students.query.get(student_id)
        if not student:
            raise ValueError(f'Student with ID {student_id} not found')
        
        # Update fields if present in data
        if 'name' in data:
            student.name = data['name']
        if 'age' in data:
            student.age = data['age']
        if 'gender' in data:
            student.gender = data['gender']
        if 'nationality' in data:
            student.nationality = data['nationality']
        if 'student_phone' in data:
            student.student_phone = data['student_phone']
        if 'parent_phone' in data:
            student.parent_phone = data['parent_phone']
        if 'notes' in data:
            student.notes = data['notes']
        if 'user_id' in data:
            student.user_id = data['user_id']
        
        # Update student plan info if provided
        if 'plan_info' in data:
            plan_data = data['plan_info']
            plan_info = students_plans_info.query.get(student_id)
            
            if plan_info:
                # Update existing plan info
                if 'last_verse_recited' in plan_data:
                    plan_info.last_verse_recited = plan_data['last_verse_recited']
                    plan_info.memorized_parts = StudentService.calculate_memorized_parts(plan_data['last_verse_recited'])
                if 'memorization_direction' in plan_data:
                    plan_info.memorization_direction = plan_data['memorization_direction']
                if 'last_verse_recited' in plan_data:
                    plan_info.last_verse_recited = plan_data['last_verse_recited']
                if 'revision_direction' in plan_data:
                    plan_info.revision_direction = plan_data['revision_direction']
                if 'new_memorization_amount' in plan_data:
                    plan_info.new_memorization_amount = plan_data['new_memorization_amount']
                if 'small_revision_amount' in plan_data:
                    plan_info.small_revision_amount = plan_data['small_revision_amount']
                if 'large_revision_amount' in plan_data:
                    plan_info.large_revision_amount = plan_data['large_revision_amount']
                if 'memorization_days' in plan_data:
                    plan_info.memorization_days = plan_data['memorization_days']
                
                plan_info.updated_at = datetime.utcnow()
            else:
                new_plan_info = students_plans_info(
                    student_id=student_id,
                    memorization_direction=plan_data.get('memorization_direction', True),
                    last_verse_recited=plan_data.get('last_verse_recited', 1),
                    revision_direction=plan_data.get('revision_direction', True),
                    new_memorization_amount=plan_data.get('new_memorization_amount'),
                    small_revision_amount=plan_data.get('small_revision_amount'),
                    large_revision_amount=plan_data.get('large_revision_amount'),
                    memorization_days=plan_data.get('memorization_days', 0),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(new_plan_info)
        
        student.updated_at = datetime.utcnow()
        db.session.commit()
        
        return student
    
    @staticmethod
    def delete_student(student_id):
        
        try:
            plan_info = students_plans_info.query.get(student_id)
            if plan_info:
                db.session.delete(plan_info)
                db.session.flush()

            student = students.query.get(student_id)
            if not student:
                raise ValueError(f'Student with ID {student_id} not found')

            db.session.delete(student)
            db.session.commit()
            
            return True
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def get_student_plan_info(student_id):
        """
        Get a student's plan info
        """
        return students_plans_info.query.get(student_id)


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

        return memorized_parts