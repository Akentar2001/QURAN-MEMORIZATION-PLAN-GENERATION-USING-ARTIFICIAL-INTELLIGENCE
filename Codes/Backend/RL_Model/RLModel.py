import sys
import os

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from RL_Model.QuranLearningEnv import QuranLearningEnv
from app import create_app 

app = create_app()
app.app_context().push()

class RLModel:
    def __init__(self):
        self.model_path = "rl_model.zip"
        if os.path.exists(self.model_path):
            self.model = PPO.load(self.model_path)
        else:
            self.model = PPO("MlpPolicy", make_vec_env(lambda: QuranLearningEnv(0, 1)))

    def get_adjustment(self, student_id, session_type):
        env = QuranLearningEnv(student_id, session_type)
        state = env.reset()
        action, _ = self.model.predict(state, deterministic=True)
        return action[0]

    def save_model(self):
        self.model.save(self.model_path)

    def train_on_student(self, student_id, session_type, total_timesteps=100):
        env = QuranLearningEnv(student_id, session_type)
        self.model.set_env(env)
        self.model.learn(total_timesteps=total_timesteps)
        self.save_model()

# Example usage:
if __name__ == "__main__":
    rl_model = RLModel()
    # Example: train on student 501 for all session types
    student_id = 501
    for session_type in [1, 2, 3]:
        rl_model.train_on_student(student_id, session_type)