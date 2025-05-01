import sys
import os

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)

from app import create_app, db
from PlanService import PlanService

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
    except Exception as e:
        print(f"An error occurred during testing: {e}")

if __name__ == "__main__":
    test_weekly_plan()