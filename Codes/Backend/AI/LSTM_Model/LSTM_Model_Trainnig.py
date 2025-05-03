import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, save_model
from tensorflow.keras.layers import LSTM, Dense, Input
import pickle
import tensorflow as tf

# Check for GPU availability and configure
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    print("GPU is available:")
    for device in physical_devices:
        print(f" - {device}")
    # Configure GPU to use memory growth
    try:
        for gpu in physical_devices:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)
else:
    print("No GPU devices available, using CPU")

# Verify GPU usage
with tf.device('/GPU:0'):
    print("TensorFlow is using GPU")
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
print("TensorFlow GPU support: ", tf.test.is_built_with_cuda())

# ========================
# 1. Load Datasets
# ========================
lessons_df = pd.read_csv('cleaned_student_data.csv', encoding='utf-8-sig')
lessons_df['date_of'] = pd.to_datetime(lessons_df['date_of'])

# ========================
# 2. Build LSTM Model
# ========================
def build_lstm_model(input_shape):
    """Build an LSTM model."""
    model = Sequential()
    model.add(Input(shape=input_shape))
    model.add(LSTM(64))
    model.add(Dense(2, activation='linear'))
    model.compile(optimizer='adam', loss='mse')
    return model

# ========================
# 3. Preprocess Data
# ========================
def preprocess_data(df, pillar_type, sequence_length):
    """Preprocess data for a specific pillar type and sequence length."""
    # Filter and reset index
    pillar_df = df[df['pillar_id'] == pillar_type].sort_values(['student_id', 'date_of']).reset_index(drop=True)
    
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
        group_indices = group.index
        if len(group_indices) < sequence_length + 1:
            continue
        
        for i in range(sequence_length, len(group_indices)):
            seq_indices = group_indices[i-sequence_length:i]
            target_index = group_indices[i]
            
            seq = scaled_features[seq_indices]
            target = scaled_features[target_index]
            sequences.append((seq, target))
    
    if not sequences:
        return np.array([]), np.array([]), scaler
    
    return np.array([s[0] for s in sequences]), np.array([s[1] for s in sequences]), scaler

# Define sequence lengths to experiment with
sequence_lengths = [3, 4, 5, 6, 7, 8, 9, 10]
best_models = {}
best_results = {}

# Train models for each sequence length
for sequence_length in sequence_lengths:
    print(f"\nTraining models with sequence length: {sequence_length}")
    
    # Preprocess for all pillars with current sequence length
    X_new, y_new, scaler_new = preprocess_data(lessons_df, 1, sequence_length)
    X_minor, y_minor, scaler_minor = preprocess_data(lessons_df, 2, sequence_length)
    X_major, y_major, scaler_major = preprocess_data(lessons_df, 3, sequence_length)
    
    # Train models only if data exists
    current_models = {}
    current_results = {}
    
    with tf.device('/GPU:0'):  # Force GPU usage
        for pillar, (X, y, scaler) in [
            (1, (X_new, y_new, scaler_new)),
            (2, (X_minor, y_minor, scaler_minor)),
            (3, (X_major, y_major, scaler_major))
        ]:
            if len(X) > 0:
                model = build_lstm_model((sequence_length, X.shape[2]))
                history = model.fit(X, y, epochs=50, batch_size=16, validation_split=0.2, verbose=1)
                val_loss = history.history['val_loss'][-1]
                
                # Store results
                current_models[pillar] = model
                current_results[pillar] = val_loss
                
                # Update best models if this performs better
                if pillar not in best_results or val_loss < best_results[pillar]:
                    best_models[pillar] = model
                    best_results[pillar] = val_loss
                    
                    # Save the best model and scaler
                    if pillar == 1:
                        model.save(f'model_new.h5')
                        with open('scaler_new.pkl', 'wb') as f:
                            pickle.dump(scaler_new, f)
                    elif pillar == 2:
                        model.save(f'model_minor.h5')
                        with open('scaler_minor.pkl', 'wb') as f:
                            pickle.dump(scaler_minor, f)
                    else:
                        model.save(f'model_major.h5')
                        with open('scaler_major.pkl', 'wb') as f:
                            pickle.dump(scaler_major, f)
                print(f"Pillar {pillar} - Validation Loss: {val_loss:.4f}")

# Print best sequence lengths for each pillar
print("\nBest performing sequence lengths:")
for pillar in best_results:
    print(f"Pillar {pillar}: Validation Loss = {best_results[pillar]:.4f}")