import numpy as np
from sqlalchemy import func
from database import Session
from models import RecitationSession, StudentsPlansInfo
import gym
from gym import spaces
from LSTMPredictor import LSTMPredictor


class QuranLearningEnv(gym.Env):
    def __init__(self, student_id: int, session_type: int):
        super().__init__()
        self.student_id = student_id
        self.session_type = session_type
        self.lstm_predictor = LSTMPredictor()
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(8,))
        self.action_space = spaces.Box(low=-0.3, high=0.3, shape=(1,))

    def reset(self):
        return self._get_state()

    def _get_state(self) -> np.ndarray:
        db_session = Session()
        try:
            plan_info = db_session.query(StudentsPlansInfo)\
                .filter(StudentsPlansInfo.student_id == self.student_id)\
                .first()

            session_count = db_session.query(func.count(RecitationSession.session_id))\
                .filter(RecitationSession.student_id == self.student_id)\
                .scalar()

            lstm_base = self.lstm_predictor.predict(self.student_id, self.session_type)
            current_amount = getattr(plan_info, self._amount_column())

            return np.array([
                plan_info.overall_rating,
                np.log(session_count + 1),
                current_amount,
                plan_info.memorization_days,
                lstm_base,
                *(np.eye(3)[self.session_type - 1])  # One-hot encoding
            ], dtype=np.float32)
        finally:
            db_session.close()

    def step(self, action):
        db_session = Session()
        try:
            plan_info = db_session.query(StudentsPlansInfo)\
                .filter(StudentsPlansInfo.student_id == self.student_id)\
                .first()

            lstm_base = self.lstm_predictor.predict(self.student_id, self.session_type)
            current_amount = getattr(plan_info, self._amount_column())
            new_amount = max(current_amount * (1 + float(action[0])), 10.0)
            
            # Apply update
            setattr(plan_info, self._amount_column(), new_amount)
            db_session.commit()

            # Calculate enhanced reward
            session = db_session.query(RecitationSession)\
                .filter(
                    RecitationSession.student_id == self.student_id,
                    RecitationSession.type == self.lstm_predictor._type_name(self.session_type)
                .order_by(RecitationSession.date.desc()))\
                .first()

            reward = self._calculate_reward(session, new_amount, lstm_base) if session else 0.0
            return self._get_state(), reward, False, {}
        finally:
            db_session.close()

    def _calculate_reward(self, session, assigned_amount: float, lstm_base: float) -> float:
        """Enhanced reward function with ambition incentives"""
        rating = session.rating / 5.0
        ambition_bonus = 0.2 * (assigned_amount / lstm_base)
        
        if rating > 0.8 and assigned_amount < lstm_base:
            penalty = 0.5 * (1 - (assigned_amount / lstm_base))
        else:
            penalty = 0.0
            
        return rating + ambition_bonus - penalty

    def _amount_column(self) -> str:
        return {1: 'new_memorization_amount', 2: 'small_revision_amount', 3: 'large_revision_amount'}[self.session_type]