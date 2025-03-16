import pandas as pd

# Load the datasets
student_lesson_history_df = pd.read_csv("Datsets\\student_lessons_history.csv")
verses_df = pd.read_excel('Datsets\\verses.xlsx')

# Create a dictionary for quick lookup on verses data
verse_info = verses_df.set_index('verse_id')[['order_in_quraan', 'reverse_index', 'letters_count', 'weight_on_page']].to_dict('index')

# Initialize lists to store calculated counts for letters and pages
calculated_letters_counts = []
calculated_pages_counts = []

# Iterate over each record in student_lesson_history_df
for index, row in student_lesson_history_df.iterrows():
    start_verse_id = row['start_verse_id']
    end_verse_id = row['end_verse_id']
    
    # Initialize counters for letters and pages
    letters_count = 0
    pages_count = 0

    # Check if the order is forward or reverse
    if start_verse_id <= end_verse_id:
        # Forward order: use order_in_quraan to select range
        start_order = verse_info[start_verse_id]['order_in_quraan']
        end_order = verse_info[end_verse_id]['order_in_quraan']
        
        # Filter verses for forward order and calculate totals
        for verse_id, verse_data in verse_info.items():
            if start_order <= verse_data['order_in_quraan'] <= end_order:
                letters_count += verse_data['letters_count']
                pages_count += verse_data['weight_on_page']
    else:
        # Reverse order: use reverse_index to select range
        start_order = verse_info[start_verse_id]['reverse_index']
        end_order = verse_info[end_verse_id]['reverse_index']
        
        # Filter verses for reverse order and calculate totals
        for verse_id, verse_data in verse_info.items():
            if start_order <= verse_data['reverse_index'] <= end_order:
                letters_count += verse_data['letters_count']
                pages_count += verse_data['weight_on_page']
    
    # Append calculated counts to lists
    calculated_letters_counts.append(letters_count)
    calculated_pages_counts.append(pages_count)



# Add calculated counts to DataFrame
student_lesson_history_df['calculated_letters_count'] = calculated_letters_counts
student_lesson_history_df['calculated_pages_count'] = calculated_pages_counts

# Drop letters_count and pages_count columns if they exist
if 'letters_count' in student_lesson_history_df.columns:
    student_lesson_history_df = student_lesson_history_df.drop('letters_count', axis=1)
if 'pages_count' in student_lesson_history_df.columns:
    student_lesson_history_df = student_lesson_history_df.drop('pages_count', axis=1)


# Update pillar_id values
student_lesson_history_df['pillar_id'] = student_lesson_history_df['pillar_id'].replace({2: 1, 4: 2})


    
# Save the updated DataFrame with new columns to a CSV file
student_lesson_history_df.to_csv('Codes\\AI\\Output\\New_Calculated_student_lessons_history.csv', index=False)