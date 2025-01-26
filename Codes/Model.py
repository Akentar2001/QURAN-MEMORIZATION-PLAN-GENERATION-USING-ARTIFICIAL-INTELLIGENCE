import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from datetime import datetime

# ========================
# 1. Data Loading & Cleaning
# ========================
# Load dataset (replace with your actual CSV path)
df = pd.read_csv('Students_Teacher 898.csv')


# Clean date column
def clean_date(date_str):
    try:
        return datetime.strptime(date_str, '%m/%d/%Y')
    except:
        return pd.NaT

df['date_of'] = df['date_of'].apply(clean_date)
df = df.dropna(subset=['date_of']).sort_values(['student_id', 'date_of'])

# ========================
# 2. Enhanced Preprocessing
# ========================
def create_sequences(group, seq_length=3):
    """Create sequences for a student's pillar-specific history"""
    features = group[['start_verse_id', 'end_verse_id', 'letters_count', 'pages_count']]
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(features)
    
    sequences = []
    for i in range(len(scaled_features) - seq_length):
        seq = scaled_features[i:i+seq_length]
        target = scaled_features[i+seq_length]
        sequences.append((seq, target, scaler))
    return sequences

# Dictionary to store all models
models = {
    2: {'model': None, 'scaler': None},  # New memorization
    3: {'model': None, 'scaler': None},  # Major revision
    4: {'model': None, 'scaler': None}   # Minor revision
}

# ========================
# 3. Model Training (All Students)
# ========================
for pillar in [2, 3, 4]:
    # Collect all sequences for this pillar type
    all_sequences = []
    scalers = []
    
    # Group by student and pillar
    grouped = df[df['pillar_id'] == pillar].groupby('student_id')
    for student_id, group in grouped:
        sequences = create_sequences(group)
        if len(sequences) > 0:
            all_sequences.extend([s[0] for s in sequences])
            scalers.append(sequences[0][2])  # Store first scaler per student
    
    if len(all_sequences) == 0:
        continue
        
    # Convert to numpy arrays
    X = np.array(all_sequences)
    y = np.array([s[1] for s in all_sequences])
    
    # Build and train model
    model = Sequential([
        LSTM(64, input_shape=(X.shape[1], X.shape[2])),
        Dense(4, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=50, batch_size=16, verbose=0)
    
    # Store model and scaler
    models[pillar]['model'] = model
    models[pillar]['scaler'] = scalers[0] if scalers else None

# ========================
# 4. Prediction Generator
# ========================
def generate_student_plan(student_id):
    """Generate complete plan for a student"""
    plan = {'student_id': student_id}
    
    for pillar in [2, 3, 4]:
        # Get student's history for this pillar
        student_data = df[(df['student_id'] == student_id) & 
                         (df['pillar_id'] == pillar)]
        
        if len(student_data) < 3 or not models[pillar]['model']:
            plan[f'pillar_{pillar}'] = "Use cluster averages (insufficient data)"
            continue
            
        # Prepare sequence
        features = student_data[['start_verse_id', 'end_verse_id', 
                               'letters_count', 
                               'pages_count']]
        scaled_seq = models[pillar]['scaler'].transform(features[-3:])
        
        # Predict
        prediction = models[pillar]['model'].predict(np.array([scaled_seq]))
        unscaled = models[pillar]['scaler'].inverse_transform(prediction)[0]
        
        plan[f'pillar_{pillar}'] = {
            'start_verse_id': int(unscaled[0]),
            'end_verse_id': int(unscaled[1]),
            'letters_count': int(unscaled[2]),
            'page_count': round(unscaled[3], 2)
        }
    
    return plan

# ========================
# 5. Generate All Plans
# ========================
all_plans = []
unique_students = df['student_id'].unique()

for student in unique_students:
    plan = generate_student_plan(student)
    all_plans.append(plan)

# Convert to DataFrame for analysis
results_df = pd.DataFrame(all_plans)
results_df.to_csv("result.csv")
print(results_df.head())