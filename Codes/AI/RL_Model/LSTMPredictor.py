import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Backend.app.Services.recitation_session_Service import RecitationSessionService

import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import pickle

class LSTMPredictor:
    def __init__(self):
        self.models = {
            1: load_model('model_new.h5'),
            2: load_model('model_minor.h5'),
            3: load_model('model_major.h5')
        }
        self.scalers = {
            1: pickle.load(open('scaler_new.pkl', 'rb')),
            2: pickle.load(open('scaler_minor.pkl', 'rb')),
            3: pickle.load(open('scaler_major.pkl', 'rb'))
        }

    def predict(self, student_id: int, session_type: int) -> float:
        
        sessions = RecitationSessionService.get_student_sessions(
            student_id=student_id,
            recitation_type=self._type_name(session_type),
            limit=3
        )

        if len(sessions) < 3:
            return max(np.mean([s.letters_count for s in sessions]) if sessions else 10.0, 10.0)

        seq_data = [s.letters_count for s in reversed(sessions)]
        scaled = self.scalers[session_type].transform(pd.DataFrame(seq_data))
        sequence = scaled.reshape(1, 3, 1)
        
        prediction = self.models[session_type].predict(sequence, verbose=0)[0][0]
        return max(self.scalers[session_type].inverse_transform([[prediction]])[0][0], 10.0)

    def _type_name(self, session_type: int) -> str:
        return {1: 'New_Memorization', 2: 'Minor_Revision', 3: 'Major_Revision'}[session_type]