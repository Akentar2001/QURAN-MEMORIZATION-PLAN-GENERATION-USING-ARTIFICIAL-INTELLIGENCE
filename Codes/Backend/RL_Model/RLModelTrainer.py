import sys
import os

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)

from datetime import datetime, timedelta
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback
from app.Services.recitation_session_Service import RecitationSessionService
# Import StudentService to get student IDs
from app.Services.Students_Services import StudentService
from QuranLearningEnv import QuranLearningEnv
import os
from datetime import datetime

class RLModelTrainer:
    def __init__(self, model_path="rl_model.zip"):
        """Initialize the RL model trainer"""
        self.model_path = model_path
        
        # Create or load the model
        if os.path.exists(model_path):
            self.model = PPO.load(model_path)
        else:
            # Initialize with default environment
            self.model = PPO(
                "MlpPolicy",
                make_vec_env(lambda: QuranLearningEnv(0, 1)),
                verbose=1,
                learning_rate=0.0003,
                n_steps=2048,
                batch_size=64,
                n_epochs=10,
                gamma=0.99,
                gae_lambda=0.95,
                clip_range=0.2,
                ent_coef=0.01
            )

    def train_on_student(self, student_id: int, session_type: int):
        """Train model on specific student's data"""
      
        env = QuranLearningEnv(student_id, session_type)

        sessions = RecitationSessionService.get_student_sessions(
            student_id=student_id,
            recitation_type=env._session_type_name(session_type),
            is_rating_not_none=True
        )

        if not sessions:
            print(f"No sessions found for student {student_id}, type {session_type}. Skipping training.") 
            return False

        eval_env = QuranLearningEnv(student_id, session_type)
        eval_callback = EvalCallback(
            eval_env,
            best_model_save_path="./best_model",
            log_path="./logs",
            eval_freq=500,
            deterministic=True,
            render=False
        )

        # Train on the collected experiences
        self.model.set_env(make_vec_env(lambda: QuranLearningEnv(student_id, session_type)))
        print(f"Training on {len(sessions)} sessions for student {student_id}, type {session_type}...") # Added print statement
        self.model.learn(
            total_timesteps=len(sessions) * 10,  # Multiple passes over the data
            callback=eval_callback
        )
        print(55555555555555555555555555555555555555555555)
        # Save the updated model
        self.model.save(self.model_path)
        print(f"Training complete for student {student_id}, type {session_type}. Model saved.") # Added print statement
        return True

    def weekly_training(self):
        """Perform training on all available data for all students"""
        print("Fetching all student IDs for weekly training...")
        try:
            # Get all student IDs
            students = StudentService.get_all_students()
            if not students:
                print("No students found. Weekly training skipped.")
                return

            student_ids = [student.student_id for student in students]
            print(f"Found {len(student_ids)} students.")

            # Train on each student and session type
            for student_id in student_ids:
                for session_type in [1, 2, 3]: # Iterate through New, Minor, Major
                    print(f"\n--- Training group: Student {student_id}, Type {session_type} ---")
                    self.train_on_student(student_id, session_type)

            print("\n--- Weekly training process finished ---")

        except Exception as e:
            print(f"An error occurred during weekly training: {e}")


    def _session_type_num(self, type_name: str) -> int:
        return {'New_Memorization': 1, 'Minor_Revision': 2, 'Major_Revision': 3}[type_name]


