import pytest
from app.services.recommendation_service import RecommendationService

def test_get_next_surah_recommendation():
    service = RecommendationService()
    recommendation = service.get_next_surah(
        student_id=1,
        current_level='beginner'
    )
    assert 'surah_number' in recommendation
    assert 'difficulty' in recommendation
    assert 'estimated_time' in recommendation

def test_get_revision_schedule():
    service = RecommendationService()
    revision = service.generate_revision_schedule(
        student_id=1,
        memorized_surahs=[1, 2, 3]
    )
    assert len(revision) > 0
    assert all('surah' in item for item in revision)
    assert all('review_date' in item for item in revision)

def test_adjust_recommendations():
    service = RecommendationService()
    adjusted = service.adjust_recommendations(
        student_id=1,
        performance_score=0.8
    )
    assert 'difficulty_adjustment' in adjusted
    assert 'pace_adjustment' in adjusted