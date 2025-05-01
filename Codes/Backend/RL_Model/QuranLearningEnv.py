import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from datetime import datetime, timedelta
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
            # start_date=cutoff_date,
            is_rating_not_none = True #!!
            # is_accepted_not_none = True
        )

        # Calculate performance metrics
        # Access attributes via s.recitation_session or s[0]
        ratings = [s.recitation_session.rating / 5.0 for s in recent_sessions if s.recitation_session.rating is not None]
        avg_rating = np.mean(ratings) if ratings else 0.0
        # Access attributes via s.recitation_session or s[0]
        success_rate = np.mean([1.0 if s.recitation_session.is_accepted else 0.0 for s in recent_sessions])
        perf_variance = np.var(ratings) if len(ratings) > 1 else 0.0

        # Get LSTM prediction
        lstm_pred = self.lstm_predictor.predict(self.student_id, self.session_type)

        # Progress indicators
        plan_info = StudentPlanInfoService.get_planInfo(student_id=self.student_id)
        # Handle potential None for plan_info
        if not plan_info:
             # Return a default state or raise an error if plan_info is crucial
             # For now, returning a zero state of the correct shape
             print(f"Warning: No plan_info found for student {self.student_id}. Returning zero state.")
             return np.zeros(self.observation_space.shape, dtype=np.float32)

        memorized_parts_percentage = (plan_info.memorized_parts / 30.0) if plan_info.memorized_parts is not None else 0.0
        session_count = RecitationSessionService.get_student_sessions_count(
            student_id=self.student_id,
            recitation_type=self._session_type_name(self.session_type),
            # start_date=cutoff_date,
            is_rating_not_none = True #!
        )
        session_count_normalized = (session_count / self.history_window) if self.history_window > 0 else 0.0
        ### ??? Is it correct - Seems reasonable if history_window is fixed

        # Session type encoding
        session_type_onehot = np.zeros(3) # Initialize with zeros
        if 1 <= self.session_type <= 3:
            session_type_onehot[self.session_type - 1] = 1.0


        # ********* I added the following values ​​as suggestions (Through AI):

        # Again
        recent_sessions2 = RecitationSessionService.get_student_sessions(
            student_id=self.student_id,
            recitation_type=self._session_type_name(self.session_type),
            # start_date=cutoff_date,
            is_accepted = True #!
        )

        # Access attributes via s.recitation_session or s[0]
        letters_counts = [s.recitation_session.letters_count for s in recent_sessions2 if s.recitation_session.letters_count is not None]
        avg_letters = np.mean(letters_counts) if letters_counts else 0.0
        letters_variance = np.var(letters_counts) if len(letters_counts) > 1 else 0.0

        # Get current letters amount - Handle potential None
        current_amount = getattr(plan_info, self._amount_column(), 0.0) # Default to 0.0 if attribute missing or None
        current_amount = current_amount if current_amount is not None else 0.0


        # Normalize letters-related features relative to LSTM prediction
        avg_letters_normalized = avg_letters / lstm_pred if lstm_pred > 0 else 0.0
        letters_variance_normalized = letters_variance / (lstm_pred ** 2) if lstm_pred > 0 else 0.0
        current_amount_normalized = current_amount / lstm_pred if lstm_pred > 0 else 0.0

        # Handle potential None for ratings
        overall_rating_section_raw = getattr(plan_info, self._rating_column(), 0.0)
        overall_rating_section = (overall_rating_section_raw / 5.0) if overall_rating_section_raw is not None else 0.0
        overall_rating = (plan_info.overall_rating / 5.0) if plan_info.overall_rating is not None else 0.0


        state_array = np.array([
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

        # Ensure the state array matches the observation space shape
        if state_array.shape != self.observation_space.shape:
            print(f"Error: State shape mismatch. Expected {self.observation_space.shape}, got {state_array.shape}")
            # Pad or truncate if necessary, or raise an error
            # For now, returning a zero state as a fallback
            return np.zeros(self.observation_space.shape, dtype=np.float32)

        return state_array

    def step(self, action):
        """Execute one time step within the environment"""
        # Get current state
        current_state = self._get_state()
        
        # Get LSTM prediction as base amount
        lstm_base = self.lstm_predictor.predict(self.student_id, self.session_type)
        
        # Calculate new amount based on action
        # Action is a percentage adjustment to the LSTM prediction
        new_amount = lstm_base * (1 + float(action[0]))
        
        # Get the latest session for this type to calculate reward
        latest_session = RecitationSessionService.get_student_sessions(
            student_id=self.student_id,
            recitation_type=self._session_type_name(self.session_type),
            limit_count=1 
        )
        latest_session = latest_session[0] if latest_session else None
        
        # Calculate reward based on session outcome
        reward = 0.0
        if latest_session:
            print("////////////////////////////////////////")
            reward = self._calculate_reward(latest_session, new_amount, lstm_base)
            
            # 1. Save current values from DB
            current_plan = StudentPlanInfoService.get_planInfo(self.student_id)
            original_amount = getattr(current_plan, self._amount_column())
            
            # 2. Update with new values temporarily
            plan_update = {
                self._amount_column(): new_amount,
            }
            StudentPlanInfoService.update_planInfo(self.student_id, plan_update)
            
            # 3. Get next state
            next_state = self._get_state()
            
            # 4. Restore original values
            restore_update = {
                self._amount_column(): original_amount,
            }
            StudentPlanInfoService.update_planInfo(self.student_id, restore_update)
        else:
            next_state = current_state
        
        # Environment never terminates
        done = False
        
        return next_state, reward, done, {}

    def _calculate_reward(self, session, assigned_amount: float, lstm_base: float) -> float:
        """Enhanced reward function with ambition incentives"""
        print("******************************")
        # Access rating via session.recitation_session or session[0]
        rating_raw = session.recitation_session.rating if session.recitation_session else None
        if rating_raw is None:
            print("Warning: Rating is None in _calculate_reward. Using 0.0.")
            rating = 0.0
        else:
            rating = rating_raw / 5.0

        # Avoid division by zero for ambition_bonus
        ambition_bonus = 0.0
        if lstm_base > 0:
             ambition_bonus = 0.2 * (assigned_amount / lstm_base)
        else:
             print("Warning: lstm_base is zero or negative in _calculate_reward.")
             # Decide how to handle this case, e.g., bonus is 0 or based on assigned_amount

        penalty = 0.0
        # Avoid division by zero for penalty
        if lstm_base > 0 and rating > 0.8 and assigned_amount < lstm_base:
            penalty = 0.5 * (1 - (assigned_amount / lstm_base))

        return rating + ambition_bonus - penalty

    def _amount_column(self) -> str:
        return {1: 'new_memorization_letters_amount', 2: 'small_revision_letters_amount', 3: 'large_revision_letters_amount'}[self.session_type]

    def _rating_column(self) -> str:
        return {1: 'overall_rating_new_memorization', 2: 'overall_rating_small_revision', 3: 'overall_rating_large_revision'}[self.session_type]

    def _session_type_name(self, session_type: int) -> str:
        return {1: 'New_Memorization', 2: 'Minor_Revision', 3: 'Major_Revision'}[session_type]