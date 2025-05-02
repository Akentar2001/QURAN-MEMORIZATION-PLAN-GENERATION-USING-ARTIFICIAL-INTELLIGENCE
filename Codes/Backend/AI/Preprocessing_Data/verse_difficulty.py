import pandas as pd

# Load datasets
cleaned_student_data = pd.read_csv('Codes\\AI\\Output\\New_Calculated_student_lessons_history.csv', encoding='utf-8-sig')
verses_df = pd.read_excel('verses.xlsx')

# Remove students with calculated_pages_count > 2 only for Pillar_id = 1
cleaned_student_data = cleaned_student_data[~((cleaned_student_data['pillar_id'] == 1) & (cleaned_student_data['calculated_pages_count'] > 2))]


# Initialize dictionary to store verse ratios
verse_ratios = {}

# Process each session with pillar_id = 1
for _, row in cleaned_student_data[cleaned_student_data['pillar_id'] == 1].iterrows():
    start_verse = row['start_verse_id']
    end_verse = row['end_verse_id']
    calculated_pages = row['calculated_pages_count']
    
    if calculated_pages <= 0:
        continue  
    
    # Fetch verses in the session
    if start_verse <= end_verse:
        # Forward order
        start_order = verses_df.loc[verses_df['verse_id'] == start_verse, 'order_in_quraan'].values[0]
        end_order = verses_df.loc[verses_df['verse_id'] == end_verse, 'order_in_quraan'].values[0]
        session_verses = verses_df[
            (verses_df['order_in_quraan'] >= start_order) & 
            (verses_df['order_in_quraan'] <= end_order)
        ].sort_values('order_in_quraan')
    else:
        # Reverse order
        start_rev = verses_df.loc[verses_df['verse_id'] == start_verse, 'reverse_index'].values[0]
        end_rev = verses_df.loc[verses_df['verse_id'] == end_verse, 'reverse_index'].values[0]
        session_verses = verses_df[
            (verses_df['reverse_index'] >= start_rev) & 
            (verses_df['reverse_index'] <= end_rev)
        ].sort_values('reverse_index')
    
    # Calculate ratio for each verse in the session
    verse_ids = session_verses['verse_id'].tolist()
    for verse_id in verse_ids:
        verse_pages = verses_df.loc[verses_df['verse_id'] == verse_id, 'weight_on_page'].values[0]
        ratio = verse_pages / calculated_pages
        if verse_id in verse_ratios:
            verse_ratios[verse_id].append(ratio)
        else:
            verse_ratios[verse_id] = [ratio]

# Compute average difficulty per verse
average_difficulty = {verse_id: sum(ratios)/len(ratios) for verse_id, ratios in verse_ratios.items()}

difficulty_df = pd.DataFrame(list(average_difficulty.items()), columns=['verse_id', 'average_difficulty'])
difficulty_df.to_csv('verse_difficulty.csv', index=False)

print("Verse difficulty calculation completed. Output saved to 'verse_difficulty.csv'.")