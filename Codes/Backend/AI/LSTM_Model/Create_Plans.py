import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
import pickle

# ------------------------
# 1. Load Datasets
# ------------------------
# Load lessons dataset
lessons_df = pd.read_csv('cleaned_student_data.csv', encoding='utf-8-sig')
lessons_df['date_of'] = pd.to_datetime(lessons_df['date_of'])

# Load verses dataset
verses_df = pd.read_excel('verses.xlsx')

# ------------------------
# 2. Load Models
# ------------------------
models = {}
scalers = {}

models[1] = load_model('model_pillar_1.h5', custom_objects={'mse': MeanSquaredError()})
models[2] = load_model('model_pillar_2.h5', custom_objects={'mse': MeanSquaredError()})
models[3] = load_model('model_pillar_3.h5', custom_objects={'mse': MeanSquaredError()})

# Load scalers
with open('scaler_pillar_1.pkl', 'rb') as f:
    scalers[1] = pickle.load(f)
with open('scaler_pillar_2.pkl', 'rb') as f:
    scalers[2] = pickle.load(f)
with open('scaler_pillar_3.pkl', 'rb') as f:
    scalers[3] = pickle.load(f)

# ----------------------------------
# 3. Generate Plans for All Pillars
# ----------------------------------
def generate_plan(student_id, pillar_id, target_letters):
    # Get last end_verse
    last_end_verse = lessons_df[(lessons_df['student_id'] == student_id) & (lessons_df['pillar_id'] == pillar_id)]['end_verse_id'].iloc[-1]
    
    # Find starting reverse_index
    order_in_quraan = verses_df[verses_df['verse_id'] == last_end_verse]['order_in_quraan'].values[0]
    current_index = order_in_quraan + 1
    
    # Accumulate verses
    accumulated_letters = 0
    accumulated_verses = []
    
    while accumulated_letters < target_letters:
        verse = verses_df[verses_df['order_in_quraan'] == current_index]
        if verse.empty:
            break
        
        accumulated_letters += verse['letters_count'].values[0]
        accumulated_verses.append(verse)
        current_index += 1
    
    # Get surah_id
    surah_ids = [verse['surah_id'].values[0] for verse in accumulated_verses]
    
    # Build output
    if not accumulated_verses:
        return {
            "start_verse": None,
            "end_verse": None,
            "total_letters": accumulated_letters,
            "verse_count": 0,
            "surah_ids": []
        }
    
    return {
        "start_verse": accumulated_verses[0]['verse_id'].values[0],
        "end_verse": accumulated_verses[-1]['verse_id'].values[0],
        "total_letters": accumulated_letters,
        "verse_count": len(accumulated_verses),
        "surah_ids": list(set(surah_ids))  # Unique surah IDs
    }

# ---------------------------------------
# 4. Generate All Plans for Each Student
# ---------------------------------------
all_plans = []
for student_id in lessons_df['student_id'].unique():
    # Initialize student plan
    student_plan = {"student_id": student_id}
    
    # Generate plans for all 3 pillars
    for pillar_id in [1, 2, 3]:  # 1=New, 2=Minor, 3=Major
        student_data = lessons_df[(lessons_df['student_id'] == student_id) & 
            (lessons_df['pillar_id'] == pillar_id)]
        
        if len(student_data) < 3:
            continue  # Skip students with insufficient data
        
        # Predict target letters
        features = student_data[['letters_count', 'pages_count']].values[-3:]
        scaled_seq = scalers[pillar_id].transform(features)
        prediction = models[pillar_id].predict(np.array([scaled_seq]))
        target_letters = scalers[pillar_id].inverse_transform(prediction)[0][0]
        
        # Generate plan for this pillar
        pillar_plan = generate_plan(student_id, pillar_id, target_letters)
        student_plan[f"pillar_{pillar_id}"] = pillar_plan
    
    # Add student plan to the list
    all_plans.append(student_plan)

# ------------------------
# 5. Save Plans to Excel
# ------------------------
output_rows = []

for plan in all_plans:
    student_id = plan['student_id']
    for pillar_id in [1, 2, 3]:
        if f"pillar_{pillar_id}" in plan:
            pillar_plan = plan[f"pillar_{pillar_id}"]
            output_rows.append({
                "student_id": student_id,
                "pillar_id": pillar_id,
                "start_verse": pillar_plan['start_verse'],
                "end_verse": pillar_plan['end_verse'],
                "total_letters": pillar_plan['total_letters'],
                "verse_count": pillar_plan['verse_count'],
                "surah_ids": ", ".join(map(str, pillar_plan['surah_ids']))
            })

output_df = pd.DataFrame(output_rows)
output_df.to_excel('quran_memorization_plans.xlsx')

print("Quran memorization plans saved to 'quran_memorization_plans.xlsx'.")
