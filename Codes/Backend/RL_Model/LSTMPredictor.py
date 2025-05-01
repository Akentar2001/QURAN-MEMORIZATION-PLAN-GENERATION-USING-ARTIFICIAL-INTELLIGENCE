import sys
import os

# Get the directory where LSTMPredictor.py is located
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
backend_path = os.path.join(project_root, 'Backend')
if backend_path not in sys.path:
     sys.path.append(backend_path)

try:
    from Backend.app.Services.recitation_session_Service import RecitationSessionService
except ImportError as e:
    print(f"Error importing RecitationSessionService: {e}")
    RecitationSessionService = None # Set to None explicitly if import fails

import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.metrics import MeanSquaredError
import pickle

class LSTMPredictor:
    def __init__(self):
        # Construct absolute paths to model and scaler files
        model_paths = {
            1: os.path.join(script_dir, 'model_new.h5'),
            2: os.path.join(script_dir, 'model_minor.h5'),
            3: os.path.join(script_dir, 'model_major.h5')
        }
        scaler_paths = {
            1: os.path.join(script_dir, 'scaler_new.pkl'),
            2: os.path.join(script_dir, 'scaler_minor.pkl'),
            3: os.path.join(script_dir, 'scaler_major.pkl')
        }

        # Check if files exist before loading
        for type_id, path in model_paths.items():
            if not os.path.exists(path):
                print(f"Error: Model file not found at {path}")
                # Handle initialization failure appropriately
                self.models = {}
                self.scalers = {}
                return # Exit init if a file is missing

        for type_id, path in scaler_paths.items():
             if not os.path.exists(path):
                 print(f"Error: Scaler file not found at {path}")
                 # Handle initialization failure appropriately
                 self.models = {}
                 self.scalers = {}
                 return # Exit init if a file is missing


        # Use MeanSquaredError class instead of string 'mse'
        custom_objects = {'mse': MeanSquaredError()}
        try:
            self.models = {
                type_id: load_model(path, custom_objects=custom_objects)
                for type_id, path in model_paths.items()
            }
            self.scalers = {
                type_id: pickle.load(open(path, 'rb'))
                for type_id, path in scaler_paths.items()
            }
        except Exception as e:
            print(f"Error loading models or scalers: {e}")
            # Handle initialization failure appropriately
            self.models = {}
            self.scalers = {}

    def predict(self, student_id: int, session_type: int) -> float:

        if RecitationSessionService is None:
             print("Error: RecitationSessionService was not imported correctly.")
             # Return a default value or raise an error, depending on desired behavior
             return 10.0 # Example default value

        if not self.models or not self.scalers or session_type not in self.models:
            print(f"Error: Model or scaler for session type {session_type} not loaded.")
            return 10.0

        
        try:
            # Call the method directly on the imported class (assuming static/class method)
            sessions = RecitationSessionService.get_student_sessions(
                student_id=student_id,
                recitation_type=self._type_name(session_type),
                limit_count=3
            )
        except Exception as e:
            print(f"Error calling RecitationSessionService.get_student_sessions: {e}")
            return 10.0 # Example default value

        if sessions is None:
             # Handle case where service method returns None unexpectedly
             print(f"Warning: get_student_sessions returned None for student {student_id}, type {session_type}")
             return 10.0 # Or raise an error, or return a default


        if len(sessions) < 3:
            # Calculate mean safely, handle empty sessions list
            # Access letters_count correctly from the session object within the tuple
            letter_counts = [s[0].letters_count for s in sessions if hasattr(s[0], 'letters_count') and s[0].letters_count is not None]
            if not letter_counts:
                print(f"Warning: No valid sessions found for student {student_id}, type {session_type} for prediction baseline.")
                return 10.0 # Default if no sessions or no letter counts
            mean_val = np.mean(letter_counts)
            print(f"Info: Less than 3 sessions found for student {student_id}, type {session_type}. Using mean: {mean_val}")
            return max(mean_val, 10.0)

        # Extract both letters_count and pages_count
        seq_data = []
        for s in reversed(sessions):
            session_obj = s[0]
            letters = getattr(session_obj, 'letters_count', None)
            pages = getattr(session_obj, 'pages_count', 0.0) # Default pages_count to 0.0 if missing
            if letters is not None:
                 # Ensure pages is treated as float if None
                 pages = pages if pages is not None else 0.0
                 seq_data.append((letters, pages))


        # Ensure seq_data has exactly 3 entries with valid data
        if len(seq_data) != 3:
             print(f"Warning: Could not form valid sequence data (length {len(seq_data)}) for student {student_id}, type {session_type}.")
             # Fallback to mean if sequence is invalid but some data exists
             if seq_data:
                 # Calculate mean of letters_count only for fallback
                 mean_val = np.mean([item[0] for item in seq_data])
                 print(f"Info: Using mean ({mean_val}) due to invalid sequence length ({len(seq_data)}).")
                 return max(mean_val, 10.0)
             else: # If still no data after filtering
                 print(f"Warning: No valid letter_counts found even with >=3 sessions for student {student_id}, type {session_type}.")
                 return 10.0 # Default if no valid data

        try:
            # Create DataFrame with both columns
            seq_data_df = pd.DataFrame(seq_data, columns=['letters_count', 'pages_count'])
            scaled = self.scalers[session_type].transform(seq_data_df)

            # Ensure sequence shape matches model input (assuming (1, 3, 2))
            if scaled.shape != (3, 2):
                 print(f"Warning: Scaled data shape mismatch {scaled.shape}, expected (3, 2) for student {student_id}, type {session_type}.")
                 # Attempt fallback to mean if possible
                 mean_val = np.mean([item[0] for item in seq_data])
                 print(f"Info: Using mean ({mean_val}) due to shape mismatch.")
                 return max(mean_val, 10.0)

            sequence = scaled.reshape(1, 3, 2) # Input shape should now be (1, 3, 2)

            # Model predicts both features, we need the first one (letters_count)
            prediction_scaled = self.models[session_type].predict(sequence, verbose=0)[0]

            # Inverse transform expects a 2D array with shape (n_samples, n_features)
            # We only predicted one step, so shape is (1, 2)
            inverted_prediction = self.scalers[session_type].inverse_transform([prediction_scaled])[0]

            # Return the first element (letters_count)
            return max(float(inverted_prediction[0]), 10.0)
        except Exception as e:
            print(f"Error during prediction/scaling for student {student_id}, type {session_type}: {e}")
            # Fallback to mean on error
            try:
                mean_val = np.mean([item[0] for item in seq_data])
                print(f"Info: Using mean ({mean_val}) due to prediction/scaling error.")
                return max(mean_val, 10.0)
            except: # If mean calculation also fails
                 print(f"Critical Error: Fallback mean calculation failed for student {student_id}, type {session_type}.")
                 return 10.0


    def _type_name(self, session_type: int) -> str:
        # Use .get for safer dictionary access
        return {1: 'New_Memorization', 2: 'Minor_Revision', 3: 'Major_Revision'}.get(session_type, 'Unknown')