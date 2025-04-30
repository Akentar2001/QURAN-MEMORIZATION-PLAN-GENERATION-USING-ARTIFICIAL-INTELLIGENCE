from datetime import datetime, timedelta
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback
from Backend.app.Services.recitation_session_Service import RecitationSessionService
from QuranLearningEnv import QuranLearningEnv
import os

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
        # Create environment for this student
        env = QuranLearningEnv(student_id, session_type)
        
        # Get recent sessions
        cutoff_date = datetime.now() - timedelta(days=7)
        sessions = RecitationSessionService.get_student_sessions(
            student_id=student_id,
            recitation_type=env._session_type_name(session_type),
            start_date=cutoff_date,
            is_rating_not_none=True
        )
        
        if not sessions:
            return False
            
        # Create evaluation callback
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
        self.model.learn(
            total_timesteps=len(sessions) * 10,  # Multiple passes over the data
            callback=eval_callback
        )
        
        # Save the updated model
        self.model.save(self.model_path)
        return True

    def weekly_training(self):
        """Perform weekly training on all available data"""
        cutoff_date = datetime.now() - timedelta(days=7)
        
        # Get all sessions from past week
        sessions = RecitationSessionService.get_student_sessions(
            #student_id
            start_date=cutoff_date,
            is_rating_not_none=True
        )
        
        if not sessions:
            return
            
        # Group sessions by student and type
        training_groups = {}
        for session in sessions:
            key = (session.student_id, self._session_type_num(session.type))
            if key not in training_groups:
                training_groups[key] = []
            training_groups[key].append(session)
            
        # Train on each group
        for (student_id, session_type), _ in training_groups.items():
            self.train_on_student(student_id, session_type)

    def _session_type_num(self, type_name: str) -> int:
        return {'New_Memorization': 1, 'Minor_Revision': 2, 'Major_Revision': 3}[type_name]