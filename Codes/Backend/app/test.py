import requests
import json

def test_get_student():
    # Test configuration
    base_url = 'http://localhost:5000/api'
    student_id = 37  # Replace with an existing student ID in your database
    
    # Test case 1: Get existing student
    try:
        response = requests.get(f'{base_url}/getStudent/{student_id}')
        print("\nTest Case 1: Get Existing Student")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("\nStudent Details:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"Error: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")

    # Test case 2: Get non-existing student
    try:
        non_existing_id = 99999
        response = requests.get(f'{base_url}/getStudent/{non_existing_id}')
        print("\nTest Case 2: Get Non-existing Student")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_get_student()