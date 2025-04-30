from app.models import students
from app import db
from app.Services.students_plans_info_services import StudentPlanInfoService
from app.Services.plan_generation_service import PlanGenerationService
from datetime import datetime
from datetime import datetime, date, timedelta

class StudentService:
    @staticmethod
    def create_student(data):
        required_fields = ['name', 'age', 'gender', 'nationality']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'Missing required field: {field}')
        try:
            new_student = students(
                name=data['name'],
                age=data['age'],
                gender=data['gender'],
                nationality=data['nationality'],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        
            optional_fields = ['student_phone', 'parent_phone', 'notes', 'user_id']
            for field in optional_fields:
                if field in data:
                    setattr(new_student, field, data[field])

            db.session.add(new_student)
            db.session.flush()
            new_student_id = new_student.student_id

            if 'plan_info' in data:
                plan_info = StudentPlanInfoService.create_planInfo(new_student.student_id, data['plan_info'])

            fake_date = "2025-03-02"  #! Change this to the desired start date
            start_date = date.fromisoformat(fake_date) if fake_date else date.today()

            plan_generator = PlanGenerationService()
            plan_generator.generate_plan(new_student.student_id, start_date=start_date)
            
            db.session.commit()

            return_student = students.query.get(new_student_id)
            return return_student
        
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error creating student: {str(e)}")
    
    @staticmethod
    def get_all_students():
        return students.query.all()
    
    @staticmethod
    def get_user_students(user_id):
        return students.query.filter(
            students.user_id == user_id
        ).all()

    @staticmethod
    def get_student_by_id(student_id):
        return students.query.filter(
            students.student_id == student_id
        ).first()
    
    @staticmethod
    def update_student(student_id, data):
        student = students.query.get(student_id)
        if not student:
            raise ValueError(f'Student with ID {student_id} not found')
        
        basic_fields = ['name', 'age', 'gender', 'nationality', 'student_phone', 
                       'parent_phone', 'notes', 'user_id']
        for field in basic_fields:
            if field in data:
                setattr(student, field, data[field])

        if 'plan_info' in data:
            StudentPlanInfoService.update_planInfo(student_id, data['plan_info'])

        student.updated_at = datetime.utcnow()
        db.session.commit()
        # student = students.query.get(student_id)
        return student

    @staticmethod
    def delete_student(student_id):
        try:
            StudentPlanInfoService.delete_planInfo(student_id)
            student = students.query.get(student_id)
            if not student:
                raise ValueError(f'Student with ID {student_id} not found')

            db.session.delete(student)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e