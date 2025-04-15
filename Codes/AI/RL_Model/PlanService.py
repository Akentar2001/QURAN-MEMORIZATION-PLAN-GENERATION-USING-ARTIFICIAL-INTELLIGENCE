from database import Session
from models import StudentsPlansInfo
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import os
from LSTMPredictor import LSTMPredictor
from QuranLearningEnv import QuranLearningEnv
from datetime import datetime


class PlanService:
    def __init__(self):
        self.rl_model = self._load_model()
        self.lstm_predictor = LSTMPredictor()
        self.last_trained = datetime.now()

    def _load_model(self):
        model_path = "rl_model.zip"
        if os.path.exists(model_path):
            return PPO.load(model_path)
        return PPO("MlpPolicy", make_vec_env(lambda: QuranLearningEnv(0, 1)))

    def generate_weekly_plans(self, student_id: int) -> dict:
        """Generate all weekly plans at once"""
        db_session = Session()
        try:
            plan_info = db_session.query(StudentsPlansInfo)\
                .filter(StudentsPlansInfo.student_id == student_id)\
                .first()

            # Generate plans for all session types
            plans = {}
            for session_type in [1, 2, 3]:
                env = QuranLearningEnv(student_id, session_type)
                state = env.reset()
                action, _ = self.rl_model.predict(state, deterministic=True)
                
                lstm_base = self.lstm_predictor.predict(student_id, session_type)
                final_amount = max(lstm_base * (1 + action[0]), 10.0)
                
                plans[self._session_type_name(session_type)] = {
                    'base': lstm_base,
                    'final': final_amount,
                    'adjustment': f"{action[0]*100:.1f}%"
                }

            # Update all amounts at once
            plan_info.new_memorization_amount = plans['New_Memorization']['final']
            plan_info.small_revision_amount = plans['Minor_Revision']['final']
            plan_info.large_revision_amount = plans['Major_Revision']['final']
            db_session.commit()

            return plans
        except Exception as e:
            db_session.rollback()
            return {"error": str(e)}
        finally:
            db_session.close()

    def _session_type_name(self, session_type: int) -> str:
        return {1: 'New_Memorization', 2: 'Minor_Revision', 3: 'Major_Revision'}[session_type]
