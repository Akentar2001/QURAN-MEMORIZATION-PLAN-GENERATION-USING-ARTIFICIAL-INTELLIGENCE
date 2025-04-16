import pytest
from app.services.student_service import StudentService

def test_get_student_progress():
    service = StudentService()
    progress = service.get_student_progress(student_id=1)
    assert 'completed_verses' in progress
    assert 'total_verses' in progress
    assert 'completion_percentage' in progress

def test_update_student_progress():
    service = StudentService()
    updated = service.update_progress(
        student_id=1,
        verses_completed=[{'surah': 1, 'verse': 1}]
    )
    assert updated is True

def test_get_student_performance():
    service = StudentService()
    performance = service.get_performance_metrics(student_id=1)
    assert 'average_retention' in performance
    assert 'completion_rate' in performance
    assert 'consistency_score' in performance