def test_plan_generation_api(client):
    response = client.post('/api/generate-plan', json={
        'student_level': 'beginner',
        'duration_weeks': 12,
        'daily_time': 30
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'plan' in data
    assert 'schedule' in data['plan']