import pandas as pd

# Load your dataset
df = pd.read_csv('cleaned_student_data.csv')

# Remove students with calculated_pages_count > 5 only for Pillar_id = 1
df = df[~((df['pillar_id'] == 1) & (df['calculated_pages_count'] > 2))]

# Save the cleaned dataset
df.to_csv('path_to_cleaned_dataset.csv', index=False)