import pandas as pd

def merge_df(lessons_df):
    # Merge lessons with verses to get Surah IDs
    lessons_df = pd.merge(
        lessons_df,
        verses_df[['verse_id', 'surah_id']],
        left_on='end_verse_id',
        right_on='verse_id',
        how='left'
    )
    return lessons_df

def clean_student_entries(lessons_df, verses_df, surahs_df, max_pages, max_letters, pillar_id, max_invalid):

    MAX_PAGES_PER_DAY = max_pages  
    MAX_LETTERS_PER_DAY = max_letters  
    
    # Track invalid entries per student
    invalid_counts = {} 

    # Group by student
    grouped = lessons_df.groupby('student_id')
    for student_id, group in grouped:
        invalid = 0
        
        # Sort by date
        group = group.sort_values('date_of')
        
        # Check for Surah sequence errors in new memorization
        new_memorization = group[group['pillar_id'] == 1]
        surah_sequence = new_memorization['surah_id'].values
        
        if len(surah_sequence) >= 2:
            # Determine memorization direction
            direction = "forward" if surah_sequence[1] > surah_sequence[0] else "reverse"
            
            # Check sequence validity
            for i in range(1, len(surah_sequence)):
                if (direction == "forward" and surah_sequence[i] < surah_sequence[i-1]) or \
                   (direction == "reverse" and surah_sequence[i] > surah_sequence[i-1]):
                    invalid += 1
        
        # Check for memorization volume violations
        volume_violations = group[
            ((group['calculated_pages_count'] > MAX_PAGES_PER_DAY) & (group['pillar_id'] == pillar_id)) |
            ((group['calculated_letters_count'] > MAX_LETTERS_PER_DAY) & (group['pillar_id'] == pillar_id))
        ]
        invalid += len(volume_violations)
        
        # Update invalid count
        invalid_counts[student_id] = invalid
    
    # Identify students to remove
    students_to_remove = [student_id for student_id, count in invalid_counts.items() if count > max_invalid]
    
    # Filter dataset
    cleaned_df = lessons_df[~lessons_df['student_id'].isin(students_to_remove)]
    
    print(f"Removed {len(lessons_df) - len(cleaned_df)} entries from {len(students_to_remove)} students")
    return cleaned_df


# Load datasets
lessons_df = pd.read_csv('Codes\\AI\\Output\\New_Calculated_student_lessons_history.csv', encoding='utf-8-sig')
verses_df = pd.read_excel('Datsets\\surahs.xlsx')
surahs_df = pd.read_excel('Datsets\\verses.xlsx')

# Clean the data
cleaned_data = merge_df(lessons_df)
cleaned_data = clean_student_entries(cleaned_data, verses_df, surahs_df, 9, 3000, 1, max_invalid=3)

cleaned_data = clean_student_entries(cleaned_data, verses_df, surahs_df, 20, 15000, 1, max_invalid=0)

cleaned_data = clean_student_entries(cleaned_data, verses_df, surahs_df, 50, 30000, 2, max_invalid=0)

cleaned_data = clean_student_entries(cleaned_data, verses_df, surahs_df, 100, 55000, 3, max_invalid=0)


# Save cleaned data
cleaned_data.to_csv('cleaned_student_data.csv', index=False)

# Optional: Validation
print("\nValidation Stats:")
print("Total students remaining:", cleaned_data['student_id'].nunique())
print("Students removed:", len(lessons_df['student_id'].unique()) - len(cleaned_data['student_id'].unique()))
