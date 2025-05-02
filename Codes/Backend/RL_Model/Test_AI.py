import sys
import os

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)

from app import create_app, db
from PlanService import PlanService
from app.Services.students_plans_info_services import StudentPlanInfoService
from app.Services.recitation_session_Service import RecitationSessionService

# Create a single application instance
app = create_app()
app.app_context().push()

# Define the test function outside the context manager
def test_weekly_plan():
    try:
        # Pass the app instance to PlanService
        plan_service = PlanService(app)
        

        # Call generate_weekly_plans with a student ID
        student_id = 501  # Replace with actual student ID

        # Get previous plan info before update
        plan_info = StudentPlanInfoService.get_planInfo(student_id)
        prev_amounts = {
            "New_Memorization": getattr(plan_info, "new_memorization_letters_amount") or getattr(plan_info, "new_memorization_pages_amount", 0) * 550,
            "Minor_Revision": getattr(plan_info, "small_revision_letters_amount") or getattr(plan_info, "minor_revision_pages_amount", 0) * 550,
            "Major_Revision": getattr(plan_info, "large_revision_letters_amount") or getattr(plan_info, "major_revision_pages_amount", 0) * 550
        }

        weekly_plans = plan_service.generate_weekly_plans(student_id)

        # Check the results
        if "error" in weekly_plans:
            print(f"Error generating weekly plans: {weekly_plans['error']}")
        else:
            print("\nWeekly Plans Generated:")
            for session_type, plan in weekly_plans.items():
                print(f"\n{session_type}:")
                print(f"Base amount: {plan['base']}")
                print(f"Final amount: {plan['final']}")
                print(f"Adjustment: {plan['adjustment']}")

                # Print percentage difference
                prev = prev_amounts.get(session_type)
                new = plan['final']
                if prev is not None and prev != 0:
                    percent_diff = ((new - prev) / prev) * 100
                    print(f"Percentage difference from previous: {percent_diff:.2f}%")
                else:
                    print("No previous amount available for percentage difference.")

                # Print average of all recitations for this session type
                recitation_type = session_type  # Should match the type name used in RecitationSessionService
                sessions = RecitationSessionService.get_student_sessions(
                    student_id=student_id,
                    recitation_type=session_type,
                    is_rating_not_none=True
                )
                letter_counts = [s[0].letters_count for s in sessions if hasattr(s[0], 'letters_count') and s[0].letters_count is not None]
                if letter_counts:
                    avg_amount = sum(letter_counts) / len(letter_counts)
                    print(f"Average amount of all recitations for this session: {avg_amount:.2f}")
                else:
                    print("No recitation data available for this session type.")
    except Exception as e:
        print(f"An error occurred during testing: {e}")

if __name__ == "__main__":
    test_weekly_plan()