from app.Services.recitation_session_Service import RecitationSessionService
from app.Services.students_plans_info_services import StudentPlanInfoService
import numpy as np
from sqlalchemy import func
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
        plan_info = StudentPlanInfoService.get_planInfo(student_id=student_id)

        session_count = get_student_sessions_count(student_id=student_id, recitation_type=self._session_type_name(self.session_type))

        lstm_base = self.lstm_predictor.predict(self.student_id, self.session_type)
        current_amount = getattr(plan_info, self._amount_column())

        return np.array([
            getattr(plan_info, self._rating_column()),
            npx.log(session_count + 1),
            current_amount,
            plan_info.memorization_days,
            lstm_base,
            *(np.eye(3)[self.session_type - 1])  # One-hot encoding
        ], dtype=np.float32)

    def step(self, action):
        plan_info = StudentPlanInfoService.get_planInfo(student_id=student_id)

        lstm_base = self.lstm_predictor.predict(self.student_id, self.session_type)
        current_amount = getattr(plan_info, self._amount_column())
        new_amount = max(current_amount * (1 + float(action[0])), 10.0)
        
        # Apply update
        setattr(plan_info, self._amount_column(), new_amount)

        session = SessionService.get_student_sessions(
            student_id=self.student_id,
            recitation_type=self.lstm_predictor._type_name(self.session_type),
            limit_count=1
        )

        reward = self._calculate_reward(session, new_amount, lstm_base) if session else 0.0
        return self._get_state(), reward, False, {}

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
        return {1: 'new_memorization_letters_amount', 2: 'small_revision_letters_amount', 3: 'large_revision_letters_amount'}[self.session_type]

    def _rating_column(self) -> str:
        return {1: 'overall_rating_new_memorization', 2: 'overall_rating_small_revision', 3: 'overall_rating_large_revision'}[self.session_type]

    def _session_type_name(self, session_type: int) -> str:
        return {1: 'New_Memorization', 2: 'Minor_Revision', 3: 'Major_Revision'}[session_type]