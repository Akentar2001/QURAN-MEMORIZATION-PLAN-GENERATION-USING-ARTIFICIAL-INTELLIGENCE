import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow.keras.models import load_model

# ========================
# 1. Load Data, Models and Scalers
# ========================
def load_test_data():
    """Load the test dataset"""
    test_df = pd.read_csv('cleaned_student_data.csv', encoding='utf-8-sig')
    test_df['date_of'] = pd.to_datetime(test_df['date_of'])
    return test_df

def load_models_and_scalers():
    """Load trained models and scalers for each pillar"""
    models = {}
    scalers = {}

    for pillar in [1, 2, 3]:
        try:
            if pillar == 1: 
                models[pillar] = load_model(f'model_new.h5', custom_objects={'mse': mean_squared_error})
                scaler_name = 'scaler_new.pkl'
            elif pillar == 2: 
                models[pillar] = load_model(f'model_minor.h5', custom_objects={'mse': mean_squared_error})
                scaler_name = 'scaler_minor.pkl'
            elif pillar == 3: 
                models[pillar] = load_model(f'model_major.h5', custom_objects={'mse': mean_squared_error})
                scaler_name = 'scaler_major.pkl'

            with open(scaler_name, 'rb') as f:
                scalers[pillar] = pickle.load(f)
        except (FileNotFoundError, IOError):
            print(f"Model or scaler for pillar {pillar} not found. Skipping.")
    
    return models, scalers

# ========================
# 2. Prepare Test Sequences
# ========================
def prepare_test_sequences(df, pillar_id, scaler, test_students=None):
    """
    Prepare test sequences for a specific pillar
    
    Parameters:
    - df: DataFrame with student data
    - pillar_id: The pillar ID to filter for
    - scaler: The scaler for this pillar's data
    - test_students: Optional list of student IDs to use for testing
    
    Returns:
    - X_test: Input sequences for testing
    - y_test: Target values for testing (letters_count only)
    - student_ids: Student IDs for each sequence
    - dates: Dates for each prediction target
    """
    # Filter for the specific pillar
    pillar_df = df[df['pillar_id'] == pillar_id].sort_values(['student_id', 'date_of']).reset_index(drop=True)
    
    if pillar_df.empty:
        return np.array([]), np.array([]), [], []
    
    # Apply the scaler - still need to scale both columns
    features = pillar_df[['letters_count', 'pages_count']]
    scaled_features = scaler.transform(features)
    
    # Create sequences
    sequences = []
    student_ids = []
    dates = []
    
    # Group by student
    grouped = pillar_df.groupby('student_id')
    for student_id, group in grouped:
        # Skip if student_id is not in test_students (if specified)
        if test_students is not None and student_id not in test_students:
            continue
            
        # Get indices
        group_indices = group.index
        if len(group_indices) < 6:  # Need at least 4 sessions for one test sequence
            continue
        
        # Use the last session as test data
        for i in range(5, len(group_indices)):
            seq_indices = group_indices[i-5:i]
            target_index = group_indices[i]
            
            seq = scaled_features[seq_indices]
            target = scaled_features[target_index, 0]  # Only take letters_count (first column)
            
            sequences.append((seq, target))
            student_ids.append(student_id)
            dates.append(pillar_df.loc[target_index, 'date_of'])
    
    if not sequences:
        return np.array([]), np.array([]), [], []
    
    X_test = np.array([s[0] for s in sequences])
    y_test = np.array([s[1] for s in sequences])
    
    return X_test, y_test, student_ids, dates

# ========================
# 3. Evaluate Model Performance
# ========================
def evaluate_model(model, X_test, y_test, scaler):
    """Evaluate model performance using multiple metrics - for letters_count only"""
    if len(X_test) == 0:
        return None, None, None
    
    # Make predictions
    y_pred_full = model.predict(X_test)
    # Extract only the letters_count prediction
    y_pred = y_pred_full[:, 0]
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Convert back to original scale for interpretability
    # We need to create dummy arrays to use with the scaler
    dummy_array_pred = np.zeros((y_pred.shape[0], 2))
    dummy_array_pred[:, 0] = y_pred
    
    dummy_array_true = np.zeros((y_test.shape[0], 2))
    dummy_array_true[:, 0] = y_test
    
    y_pred_original = scaler.inverse_transform(dummy_array_pred)[:, 0]
    y_test_original = scaler.inverse_transform(dummy_array_true)[:, 0]
    
    # Calculate metrics in original scale
    mse_original = mean_squared_error(y_test_original, y_pred_original)
    mae_original = mean_absolute_error(y_test_original, y_pred_original)
    
    return {
        'scaled': {
            'mse': mse,
            'mae': mae,
            'r2': r2
        },
        'original': {
            'mse': mse_original,
            'mae': mae_original,
            'r2': r2_score(y_test_original, y_pred_original)
        },
        'predictions': {
            'scaled': {
                'true': y_test,
                'pred': y_pred
            },
            'original': {
                'true': y_test_original,
                'pred': y_pred_original
            }
        }
    }

# ========================
# 4. Visualize Results
# ========================
def visualize_predictions(results, pillar_id):
    """Visualize predictions vs actual values for letters_count only"""
    if results is None or 'predictions' not in results:
        print(f"No results to visualize for pillar {pillar_id}")
        return
    
    predictions = results['predictions']['original']
    
    # Letters Count: Predicted vs Actual
    plt.figure(figsize=(12, 6))
    plt.scatter(predictions['true'], predictions['pred'], alpha=0.6)
    
    # Draw the perfect prediction line (x=y)
    min_val = min(min(predictions['true']), min(predictions['pred']))
    max_val = max(max(predictions['true']), max(predictions['pred']))
    plt.plot([min_val, max_val], [min_val, max_val], 'r--')
    
    plt.title(f'Pillar {pillar_id}: Predicted vs Actual Letters Count')
    plt.xlabel('Actual Letters Count')
    plt.ylabel('Predicted Letters Count')
    plt.savefig(f'pillar_{pillar_id}_letters_pred_vs_actual.png')
    
    # Error Distribution
    plt.figure(figsize=(12, 6))
    errors = predictions['pred'] - predictions['true']
    plt.hist(errors, bins=30, alpha=0.7)
    plt.title(f'Pillar {pillar_id}: Error Distribution (Letters Count)')
    plt.xlabel('Prediction Error')
    plt.ylabel('Frequency')
    plt.axvline(x=0, color='r', linestyle='--')
    plt.savefig(f'pillar_{pillar_id}_letters_error_dist.png')

# ========================
# 5. Student-Level Analysis
# ========================
def analyze_student_performance(results, student_ids, dates, pillar_id):
    """Analyze model performance at the student level for letters_count only"""
    if results is None or 'predictions' not in results or len(student_ids) == 0:
        print(f"No student data to analyze for pillar {pillar_id}")
        return
    
    predictions = results['predictions']['original']
    
    # Create DataFrame for analysis
    student_results = pd.DataFrame({
        'student_id': student_ids,
        'date': dates,
        'actual_letters': predictions['true'],
        'pred_letters': predictions['pred']
    })
    
    # Calculate errors
    student_results['error_letters'] = student_results['pred_letters'] - student_results['actual_letters']
    student_results['abs_error_letters'] = abs(student_results['error_letters'])
    student_results['error_percentage'] = (student_results['error_letters'] / student_results['actual_letters']) * 100
    student_results.loc[student_results['actual_letters'] == 0, 'error_percentage'] = np.nan
    
    # Group by student and get average errors
    student_avg_errors = student_results.groupby('student_id').agg({
        'abs_error_letters': 'mean',
        'error_letters': 'mean',  # Check for bias
        'error_percentage': 'mean'
    }).reset_index()
    
    # Sort by error to see which students have largest errors
    student_avg_errors_sorted = student_avg_errors.sort_values('abs_error_letters', ascending=False)
    
    # Save to CSV
    student_avg_errors_sorted.to_csv(f'pillar_{pillar_id}_student_errors.csv', index=False)
    
    # Plot errors over time
    plt.figure(figsize=(12, 6))
    student_results.sort_values('date', inplace=True)
    
    # Get 5 most frequent students
    top_students = student_results['student_id'].value_counts().nlargest(5).index
    
    for student in top_students:
        student_data = student_results[student_results['student_id'] == student]
        plt.plot(student_data['date'], student_data['abs_error_letters'], 'o-', label=f'Student {student}')
    
    plt.title(f'Pillar {pillar_id}: Absolute Error Over Time (Top 5 Students)')
    plt.xlabel('Date')
    plt.ylabel('Absolute Error (Letters)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'pillar_{pillar_id}_errors_over_time.png')
    
    return student_results

# ========================
# 6. Threshold Analysis
# ========================
def threshold_analysis(all_results):
    """Analyze success rate based on various error thresholds for letters_count only"""
    for pillar_id, results in all_results.items():
        if results is None:
            continue
            
        predictions = results['predictions']['original']
        
        # Letters count thresholds
        letters_errors = abs(predictions['pred'] - predictions['true'])
        
        thresholds = [10, 25, 50, 100, 200]
        print(f"\nThreshold Analysis for Pillar {pillar_id} (Letters Count):")
        for threshold in thresholds:
            success_rate = (letters_errors <= threshold).mean() * 100
            print(f"Success rate within {threshold} letters: {success_rate:.2f}%")
        
        # Percentage error thresholds
        percentage_errors = abs((predictions['pred'] - predictions['true']) / predictions['true']) * 100
        # Replace inf values with NaN
        percentage_errors = np.where(np.isinf(percentage_errors), np.nan, percentage_errors)
        
        thresholds = [5, 10, 20, 50, 100]
        print(f"\nThreshold Analysis for Pillar {pillar_id} (Percentage Error):")
        for threshold in thresholds:
            # Filter out NaN values
            valid_errors = percentage_errors[~np.isnan(percentage_errors)]
            if len(valid_errors) > 0:
                success_rate = (valid_errors <= threshold).mean() * 100
                print(f"Success rate within {threshold}% error: {success_rate:.2f}%")
            else:
                print(f"No valid data for {threshold}% threshold")

# ========================
# 7. Main Testing Function
# ========================
def test_models():
    """Main function to test all models - focusing on letters_count only"""
    # Load data, models and scalers
    test_df = load_test_data()
    models, scalers = load_models_and_scalers()
    
    # Store results for comparison
    all_results = {}
    
    # Test each pillar
    for pillar_id in [1, 2, 3]:
        if pillar_id not in models or pillar_id not in scalers:
            print(f"Skipping pillar {pillar_id} due to missing model or scaler")
            continue
        
        print(f"\n{'='*50}")
        print(f"Testing model for Pillar {pillar_id}")
        print(f"{'='*50}")
        
        # Prepare test sequences
        X_test, y_test, student_ids, dates = prepare_test_sequences(
            test_df, pillar_id, scalers[pillar_id]
        )
        
        if len(X_test) == 0:
            print(f"No test data available for pillar {pillar_id}")
            continue
            
        print(f"Number of test sequences: {len(X_test)}")
        
        # Evaluate model
        results = evaluate_model(models[pillar_id], X_test, y_test, scalers[pillar_id])
        all_results[pillar_id] = results
        
        # Print metrics
        print("\nModel Performance Metrics (Letters Count Only):")
        print(f"Scaled MSE: {results['scaled']['mse']:.6f}")
        print(f"Scaled MAE: {results['scaled']['mae']:.6f}")
        print(f"R-squared (scaled): {results['scaled']['r2']:.6f}")
        print(f"Original MSE: {results['original']['mse']:.2f}")
        print(f"Original MAE: {results['original']['mae']:.2f}")
        print(f"R-squared (original): {results['original']['r2']:.6f}")
        
        # Visualize results
        visualize_predictions(results, pillar_id)
        
        # Student-level analysis
        student_results = analyze_student_performance(results, student_ids, dates, pillar_id)
    
    # Compare pillars
    if len(all_results) > 0:
        print("\n\n")
        print(f"{'='*50}")
        print(f"Comparing Pillar Models (Letters Count Only)")
        print(f"{'='*50}")
        
        for pillar_id, results in all_results.items():
            if results is None:
                continue
            print(f"\nPillar {pillar_id}:")
            print(f"R-squared: {results['original']['r2']:.6f}")
            print(f"MAE: {results['original']['mae']:.2f}")
    
    # Run threshold analysis
    threshold_analysis(all_results)
    
    return all_results

# ========================
# 8. New Student Prediction Function
# ========================
def predict_letters_for_new_student(student_id, pillar_id, last_3_sessions, model, scaler):
    """
    Predict next session letters count for a specific student and pillar
    
    Parameters:
    - student_id: ID of the student
    - pillar_id: Pillar type to predict for
    - last_3_sessions: List of tuples (letters_count, pages_count) for last 3 sessions
    - model: Trained model for this pillar
    - scaler: Scaler for this pillar
    
    Returns:
    - Predicted letters_count for next session
    """
    # Convert to array
    last_3_sessions_array = np.array(last_3_sessions)
    
    # Scale the input
    scaled_input = scaler.transform(last_3_sessions_array)
    
    # Reshape for LSTM (samples, time steps, features)
    X_input = scaled_input.reshape(1, 3, 2)
    
    # Make prediction
    scaled_prediction = model.predict(X_input)[0]
    
    # Convert back to original scale
    dummy_array = np.zeros((1, 2))
    dummy_array[0, 0] = scaled_prediction[0]  # Only take letters_count prediction
    
    prediction_original = scaler.inverse_transform(dummy_array)[0, 0]
    
    return prediction_original

# Run the tests
if __name__ == "__main__":
    all_results = test_models()
    
    # Example of prediction for a new student
    # (This would use real data in practice)
    models, scalers = load_models_and_scalers()
    
    if 1 in models and 1 in scalers:
        sample_student_sessions = [
            (120, 0.25),  # First session
            (150, 0.30),  # Second session
            (140, 0.28)   # Third session
        ]
        
        prediction = predict_letters_for_new_student(
            student_id=9999,
            pillar_id=1,
            last_3_sessions=sample_student_sessions,
            model=models[1],
            scaler=scalers[1]
        )
        
        print("\nSample prediction for a new student:")
        print(f"Last 3 sessions: {sample_student_sessions}")
        print(f"Predicted next session letters count = {prediction:.2f}")