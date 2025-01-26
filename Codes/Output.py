
import pandas as pd
import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras.losses import MeanSquaredError

# Load the saved model
model = tf.keras.models.load_model(
    'quranic_lstm_model.h5',
    custom_objects={'mse': MeanSquaredError()}
)

# Load the pillar_id encoder
with open('pillar_id_encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

# Reload the dataset
file_path = "C:\\Users\\aqint\\Downloads\\csv_recitations.csv"  # Update with your file path
data = pd.read_csv(file_path)

# Check for missing values and drop them
data = data.dropna()

# Encode pillar_id as numeric values
data['pillar_id'] = encoder.transform(data['pillar_id'])

# Create Sequences for Prediction
def create_sequences_for_prediction(grouped_data, seq_length=5):
    sequences = []
    student_ids = []
    pillar_ids = []
    
    for (student_id, pillar_id), group in grouped_data:
        # Sort the group by date
        group = group.sort_values('date_of').reset_index(drop=True)
        
        for i in range(len(group) - seq_length):
            seq = group[['letters_count', 'pages_count']].iloc[i:i + seq_length].values
            sequences.append(seq)
            student_ids.append(student_id)
            pillar_ids.append(pillar_id)
    
    return sequences, student_ids, pillar_ids

# Group data by student_id and pillar_id
grouped_data = data.groupby(['student_id', 'pillar_id'])

# Generate sequences and related information
seq_length = 5
sequences, student_ids, pillar_ids = create_sequences_for_prediction(grouped_data, seq_length)

# Convert to NumPy arrays
sequences = np.array(sequences)

# Make Predictions
predictions = model.predict(sequences)

# Load verses metadata
verses_file = "C:\\Users\\aqint\\Downloads\\verses.csv"  # Update with your file path
verses = pd.read_csv(verses_file)

# Prepare Results DataFrame
results = pd.DataFrame({
    'student_id': student_ids,
    'pillar_id': [encoder.inverse_transform([p])[0] for p in pillar_ids],  # Decode pillar_id
    'predicted_letters_count': predictions[:, 0],
    'predicted_pages_count': predictions[:, 1]
})

# Function to determine the next recitation range
def determine_recitation_range(verses, last_verse_id, predicted_letters, predicted_pages):
    last_verse_index = verses.loc[verses['verse_id'] == last_verse_id, 'reverse_index'].values[0]
    next_index = last_verse_index + 1
    total_letters = 0
    total_pages = 0
    start_verse = None
    end_verse = None

    for i in range(next_index, len(verses)):
        verse = verses.iloc[i]
        total_letters += verse['letters_count']
        total_pages += verse['weight_on_page']
        
        if start_verse is None:
            start_verse = verse['verse_id']
        
        if total_letters >= predicted_letters or total_pages >= predicted_pages:
            end_verse = verse['verse_id']
            break

    #surah_names = verses.loc[verses['verse_id'].between(start_verse, end_verse), 'surah_name'].unique()
    #pages = verses.loc[verses['verse_id'].between(start_verse, end_verse), 'page'].unique()

    return start_verse, end_verse
# Apply the logic to each student
results['start_verse'] = None
results['end_verse'] = None
#results['surah_names'] = None
#results['pages'] = None

for idx, row in results.iterrows():
    student_last_verse = data.loc[data['student_id'] == row['student_id'], 'end_verse_id'].max()
    start_verse, end_verse= determine_recitation_range(
        verses,
        student_last_verse,
        row['predicted_letters_count'],
        row['predicted_pages_count']
    )
    results.at[idx, 'start_verse'] = start_verse
    results.at[idx, 'end_verse'] = end_verse
    #results.at[idx, 'surah_names'] = ", ".join(surah_names)
    #
    # results.at[idx, 'pages'] = ", ".join(map(str, pages))

# Display Results
for student_id, student_group in results.groupby('student_id'):
    print(f"\nStudent ID: {student_id}")
    print(student_group[['pillar_id', 'predicted_letters_count', 'predicted_pages_count', 
                         'start_verse', 'end_verse']])