from datetime import datetime, timedelta
from database import Session
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from models import RecitationSession



class RLModelTrainer:
    def __init__(self):
        self.model = PPO("MlpPolicy", make_vec_env(lambda: QuranLearningEnv(0, 1)))

    def weekly_training(self):
        """Aggregate weekly data and train"""
        db_session = Session()
        try:
            # Get all sessions from the past week
            cutoff_date = datetime.now() - timedelta(days=7)
            sessions = db_session.query(RecitationSession)\
                .filter(RecitationSession.date >= cutoff_date)\
                .all()

            # Train on new experiences
            for session in sessions:
                env = QuranLearningEnv(session.student_id, self._session_type_num(session.type))
                state = env.reset()
                next_state, reward, done, _ = env.step([session.RL_reward_signal])
                self.model.replay_buffer.add(state, next_state, [session.RL_reward_signal], reward, done)

            self.model.learn(total_timesteps=len(sessions))
            self.model.save("rl_model.zip")
        finally:
            db_session.close()

    def _session_type_num(self, type_name: str) -> int:
        return {'New_Memorization': 1, 'Minor_Revision': 2, 'Major_Revision': 3}[type_name]
