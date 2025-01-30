# -*- coding: utf-8 -*-
"""LSTM Model Training for Quran Memorization Plans"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, save_model
from tensorflow.keras.layers import LSTM, Dense
import pickle

# ========================
# 1. Load Datasets
# ========================
lessons_df = pd.read_csv('cleaned_student_data.csv', encoding='utf-8-sig')
lessons_df['date_of'] = pd.to_datetime(lessons_df['date_of'])

# ========================
# 2. Preprocess Data (Fixed Index Alignment)
# ========================
def preprocess_data(df, pillar_type):
    """Preprocess data for a specific pillar type."""
    # Filter and reset index
    pillar_df = df[df['pillar_id'] == pillar_type].sort_values(['student_id', 'date_of']).reset_index(drop=True)
    
    # Skip if no data
    if pillar_df.empty:
        return np.array([]), np.array([]), None
    
    # Normalize features
    scaler = MinMaxScaler()
    features = pillar_df[['letters_count', 'pages_count']]
    scaled_features = scaler.fit_transform(features)
    
    # Create sequences
    sequences = []
    grouped = pillar_df.groupby('student_id')
    for student_id, group in grouped:
        # Get indices relative to pillar_df (not original lessons_df)
        group_indices = group.index
        if len(group_indices) < 3:
            continue  # Skip students with <3 sessions
        
        for i in range(3, len(group_indices)):
            seq_indices = group_indices[i-3:i]
            target_index = group_indices[i]
            
            # Ensure indices are within bounds
            if target_index >= len(scaled_features):
                continue
                
            seq = scaled_features[seq_indices]
            target = scaled_features[target_index]
            sequences.append((seq, target))
    
    if not sequences:
        return np.array([]), np.array([]), scaler
    
    return np.array([s[0] for s in sequences]), np.array([s[1] for s in sequences]), scaler

# ========================
# 3. Build & Train LSTM Models
# ========================
def build_lstm_model(input_shape):
    """Build an LSTM model."""
    model = Sequential([
        LSTM(64, input_shape=input_shape),
        Dense(2, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# Preprocess for all pillars
X_new, y_new, scaler_new = preprocess_data(lessons_df, 1)
X_minor, y_minor, scaler_minor = preprocess_data(lessons_df, 2)
X_major, y_major, scaler_major = preprocess_data(lessons_df, 3)


# Train models only if data exists
models = {}
if len(X_new) > 0:
    models[1] = build_lstm_model((X_new.shape[1], X_new.shape[2]))
    models[1].fit(X_new, y_new, epochs=50, batch_size=16, verbose=0)
if len(X_minor) > 0:
    models[2] = build_lstm_model((X_minor.shape[1], X_minor.shape[2]))
    models[2].fit(X_minor, y_minor, epochs=50, batch_size=16, verbose=0)
if len(X_major) > 0:
    models[3] = build_lstm_model((X_major.shape[1], X_major.shape[2]))
    models[3].fit(X_major, y_major, epochs=50, batch_size=16, verbose=0)

# ========================
# 4. Save Models & Scalers
# ========================
for pillar in models:
    save_model(models[pillar], f'model_pillar_{pillar}.h5')
    with open(f'scaler_pillar_{pillar}.pkl', 'wb') as f:
        if pillar == 2:
            pickle.dump(scaler_new, f)
        elif pillar == 3:
            pickle.dump(scaler_major, f)
        else:
            pickle.dump(scaler_minor, f)