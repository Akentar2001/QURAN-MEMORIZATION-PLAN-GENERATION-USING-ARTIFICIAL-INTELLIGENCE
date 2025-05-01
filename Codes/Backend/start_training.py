import sys
import os

# Ensure the RL_Model and app directories are in the Python path
backend_path = os.path.dirname(os.path.abspath(__file__))
rl_model_path = os.path.join(backend_path, 'RL_Model')
if rl_model_path not in sys.path:
    sys.path.insert(0, rl_model_path)
if backend_path not in sys.path:
     sys.path.insert(0, backend_path)

from RL_Model.RLModelTrainer import RLModelTrainer
from app import create_app # Import create_app to initialize Flask context if needed by services

# Create and push Flask app context if services require it
app = create_app()
app.app_context().push()

if __name__ == "__main__":
    print("Initializing RL Model Trainer...")
    trainer = RLModelTrainer()

    # --- Choose one of the training methods ---

    # Option 1: Perform weekly training on all recent data
    # print("Starting weekly training...")
    # trainer.weekly_training()
    # print("Weekly training finished.")

    # Option 2: Train on a specific student for ALL session types
    student_id_to_train = 501 # Replace with the actual student ID
    print(f"Starting training for student {student_id_to_train} on all session types...")
    for session_type_to_train in [1, 2, 3]: # Loop through New_Memorization, Minor_Revision, Major_Revision
        print(f"--- Training type {session_type_to_train} ---")
        success = trainer.train_on_student(student_id_to_train, session_type_to_train)
        if success:
            print(f"Training for type {session_type_to_train} finished successfully.")
        else:
            print(f"No recent sessions found for type {session_type_to_train}. Training skipped.")
    print(f"Training for student {student_id_to_train} completed.")

    print("Training script completed.")