from app.models import students
from app import db
from app.models import students_plans_info
from datetime import datetime

class StudentService:
    @staticmethod
    def create_student(data):
        """
        Create a new student in the database along with their plan info
        """
        # Validate required fields for student
        required_fields = ['name', 'age', 'gender', 'nationality']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'Missing required field: {field}')
        
        # Create new student
        new_student = students(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            nationality=data['nationality'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Add optional fields if present
        if 'student_phone' in data:
            new_student.student_phone = data['student_phone']
        if 'parent_phone' in data:
            new_student.parent_phone = data['parent_phone']
        if 'notes' in data:
            new_student.notes = data['notes']
        if 'memorized_parts' in data:
            new_student.memorized_parts = data['memorized_parts']
        if 'user_id' in data:
            new_student.user_id = data['user_id']
        def set_last_verse_recited(start_surah,no_verse_in_surah):
            
            verse_id = verses.query.filter_by(name = start_surah, order_in_surah = no_verse_in_surah).first()
            return verse_id

        #----------------------------------------------------------------
        if 'memorization_direction' in data:
            new_student.memorization_direction=data['memorization_direction']
        if 'last_verse_recited' in data:
            new_student.last_verse_recited=data['last_verse_recited']
        if 'revision_direction' in data:
            new_student.revision_direction=data['revision_direction']
        if 'new_memorization_amount' in data:
            new_student.new_memorization_amount=data['new_memorization_amount']
        if'small_revision_amount' in data:
            new_student.small_revision_amount=data['small_revision_amount']
        if 'large_revision_amount' in data:
            new_student.large_revision_amount=data['large_revision_amount']
        if'memorization_days' in data:
            new_student.memorization_days=data['memorization_days']

        # Add to database
        db.session.add(new_student)
        db.session.commit()
        
        return new_student
    
    @staticmethod
    def get_all_students():
        """
        Get all students from the database
        """
        return students.query.all()
    
    @staticmethod
    def get_student_by_id(student_id):
        """
        Get a student by ID
        """
        return students.query.get(student_id)
    
    @staticmethod
    def update_student(student_id, data):
        """
        Update a student's information
        """
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
        if 'memorized_parts' in data:
            student.memorized_parts = data['memorized_parts']
        if 'user_id' in data:
            student.user_id = data['user_id']
        
        # Update student plan info if provided
        if 'plan_info' in data:
            plan_data = data['plan_info']
            plan_info = students_plans_info.query.get(student_id)
            
            if plan_info:
                # Update existing plan info
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
                # Create new plan info if it doesn't exist
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
        """
        Delete a student from the database
        """
        student = students.query.get(student_id)
        if not student:
            raise ValueError(f'Student with ID {student_id} not found')
        
        # StudentPlanInfo will be automatically deleted due to CASCADE
        db.session.delete(student)
        db.session.commit()
        
        return True
        
    @staticmethod
    def get_student_plan_info(student_id):
        """
        Get a student's plan info
        """
        return students_plans_info.query.get(student_id)