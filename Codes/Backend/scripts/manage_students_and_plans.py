import sys
import os

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)

from app import create_app
from app.Services.plan_generation_service import PlanGenerationService
from app.Services.Students_Services import StudentService
from datetime import date

app = create_app()
app.app_context().push()

def generate_plan_for_student(student_id, start_date=None):
    try:
        if start_date is None:
            fake_date = "2025-03-09"
            start_date = date.fromisoformat(fake_date)
            # start_date = date(2025, 3, 9)  #! You can modify this date
        
        plan_generator = PlanGenerationService()
        plan_generator.generate_plan(
            student_id=student_id, 
            start_date=start_date
        )
        print(f"Successfully generated plan for student {student_id}")
    except Exception as e:
        print(f"Error generating plan for student {student_id}: {str(e)}")

def add_new_student():
    try:
        student_data = {
            'name': input("Enter student name: "),
            'age': int(input("Enter student age: ")),
            'gender': input("Enter student gender (M/F): "),
            'nationality': input("Enter student nationality: "),
            'plan_info': {
                'start_surah': int(input("Enter starting surah number: ")),
                'no_verse_in_surah': int(input("Enter starting verse number: ")),
                'memorization_direction': input("Enter memorization direction (ASC/DESC): "),
                'revision_direction': input("Enter revision direction (ASC/DESC): "),
                'memorization_days': int(input("Enter sum number of memorization days per week (from Sunday, 1-2-4-8-16-32-64): ") or 5)
            }
        }
        
        new_student = StudentService.create_student(student_data)
        print(f"Successfully added student with ID: {new_student.student_id}")
        return new_student.student_id
    except Exception as e:
        print(f"Error adding student: {str(e)}")
        return None

def generate_plans_for_all_students():
    try:
        students = StudentService.get_all_students()
        fake_date = "2025-03-09"
        start_date = date.fromisoformat(fake_date)
        # start_date = date(2025, 3, 9)  #! You can modify this date
        
        print(f"Generating plans for {len(students)} students...")
        for student in students:
            generate_plan_for_student(student.student_id, start_date)
            
        print("Completed generating plans for all students")
    except Exception as e:
        print(f"Error generating plans for all students: {str(e)}")

def main():
    while True:
        print("\nStudent Plan Management System")
        print("1. Generate plan for specific student")
        print("2. Add new student")
        print("3. Generate plans for all students")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            student_id = int(input("Enter student ID: "))
            year = int(input("Enter year (YYYY): "))
            month = int(input("Enter month (1-12): "))
            day = int(input("Enter day (1-31): "))
            generate_plan_for_student(student_id, date(year, month, day))
        
        elif choice == "2":
            student_id = add_new_student()
            if student_id and input("Generate plan for new student? (y/n): ").lower() == 'y':
                generate_plan_for_student(student_id)
        
        elif choice == "3":
            generate_plans_for_all_students()
        
        elif choice == "4":
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()