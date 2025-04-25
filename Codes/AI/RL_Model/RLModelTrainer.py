from datetime import datetime, timedelta
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from app.Services.recitation_session_Service import RecitationSessionService

class RLModelTrainer:
    def __init__(self):
        self.model = PPO("MlpPolicy", make_vec_env(lambda: QuranLearningEnv(0, 1)))

    def weekly_training(self):
        """Aggregate weekly data and train"""
        # Get all sessions from the past week
        cutoff_date = datetime.now() - timedelta(days=7)

        plan_info = StudentPlanInfoService.get_planInfo(student_id=student_id)
        RL_last_action = plan_info.rl_last_action

        sessions = RecitationSessionService.get_student_sessions(
            student_id=self.student_id,
            start_date=cutoff_date
        )

        # Train on new experiences
        for session in sessions:
            env = QuranLearningEnv(session.student_id, self._session_type_num(session.type))
            state = env.reset()
            # next_state, reward, done, _ = env.step([session.RL_reward_signal])
            # self.model.replay_buffer.add(state, next_state, [session.RL_reward_signal], reward, done)
            next_state, reward, done, _ = env.step([RL_last_action])
            self.model.replay_buffer.add(state, next_state, [RL_last_action], reward, done)

        self.model.learn(total_timesteps=len(sessions))
        self.model.save("rl_model.zip")

    def _session_type_num(self, type_name: str) -> int:
        return {'New_Memorization': 1, 'Minor_Revision': 2, 'Major_Revision': 3}[type_name]
