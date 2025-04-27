from Backend.app.Services.recitation_session_Service import RecitationSessionService
from Backend.app.Services.students_plans_info_services import StudentPlanInfoService
import numpy as np
from sqlalchemy import func
import gym
from gym import spaces
from LSTMPredictor import LSTMPredictor


class QuranLearningEnv(gym.Env):
    def __init__(self, student_id: int, session_type: int, history_window: int = 7):
        super().__init__()
        self.student_id = student_id
        self.session_type = session_type
        self.history_window = history_window
        self.lstm_predictor = LSTMPredictor()

        # Define state space with 10 dimensions
        self.observation_space = spaces.Box(
            low=np.array([
                0.0,    # Average rating (0-1)
                0.0,    # Success rate (0-1)
                0.0,    # Performance variance
                0.0,    # LSTM prediction (normalized)
                0.0,    # Memorized Parts
                0.0,    # Normalized session count
                0.0,    # avg_letters_normalized
                0.0,    # letters_variance_normalized
                0.0,    # current_amount_normalized
                0.0,    # Overall rating for this session type
                0.0,    # Overall general rating
                0.0,    # Session type one-hot (3 dimensions)
                0.0,
                0.0,
            ], dtype=np.float32),
            high=np.array([1.0] * 14, dtype=np.float32)
        )
        
        self.action_space = spaces.Box(
            low=-0.3,
            high=0.3,
            shape=(1,)
        )

    def reset(self):
        return self._get_state()

    def _get_state(self) -> np.ndarray:
        # Get recent sessions
        recent_sessions = RecitationSessionService.get_student_sessions(
            student_id=self.student_id,
            recitation_type=self._session_type_name(self.session_type),
            start_date=cutoff_date,
            is_rating_not_none = True #!!
            # is_accepted_not_none = True 
        )
        
        # Calculate performance metrics
        ratings = [s.rating/5.0 for s in recent_sessions if s.rating is not None]
        avg_rating = np.mean(ratings) if ratings else 0.0
        success_rate = np.mean([1.0 if s.is_accepted else 0.0 for s in recent_sessions])
        perf_variance = np.var(ratings) if len(ratings) > 1 else 0.0

        # Get LSTM prediction
        lstm_pred = self.lstm_predictor.predict(self.student_id, self.session_type)

        # Progress indicators
        plan_info = StudentPlanInfoService.get_planInfo(student_id=self.student_id)
        memorized_parts_percentage = plan_info.memorized_parts / 30.0
        session_count = RecitationSessionService.get_student_sessions_count(
            student_id=self.student_id,
            recitation_type=self._session_type_name(self.session_type),
            start_date=cutoff_date,
            is_rating_not_none = True #!
        )
        session_count_normalized = session_count / history_window
        ### ??? Is it correct

        # Session type encoding
        session_type_onehot = np.eye(3)[self.session_type - 1]

        # ********* I added the following values ​​as suggestions (Through AI):

        # Again 
        recent_sessions2 = RecitationSessionService.get_student_sessions(
            student_id=self.student_id,
            recitation_type=self._session_type_name(self.session_type),
            start_date=cutoff_date,
            is_accepted = True #!
        )

        letters_counts = [s.letters_count for s in recent_sessions2]
        avg_letters = np.mean(letters_counts) if letters_counts else 0.0
        letters_variance = np.var(letters_counts) if len(letters_counts) > 1 else 0.0
        
        # Get current letters amount
        current_amount = getattr(plan_info, self._amount_column())
        
        # Normalize letters-related features relative to LSTM prediction        
        avg_letters_normalized = avg_letters / lstm_pred if lstm_pred > 0 else 0.0
        letters_variance_normalized = letters_variance / (lstm_pred ** 2) if lstm_pred > 0 else 0.0
        current_amount_normalized = current_amount / lstm_pred if lstm_pred > 0 else 0.0

        overall_rating_section = getattr(plan_info, self._rating_column()) / 5.0  # Normalize to 0-1
        overall_rating = plan_info.overall_rating / 5.0  # Normalize to 0-1

        return np.array([
            avg_rating,
            success_rate,
            perf_variance,
            lstm_pred,
            memorized_parts_percentage,
            session_count_normalized,
            avg_letters_normalized,
            letters_variance_normalized,
            current_amount_normalized,
            overall_rating_section,
            overall_rating,
            *session_type_onehot
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