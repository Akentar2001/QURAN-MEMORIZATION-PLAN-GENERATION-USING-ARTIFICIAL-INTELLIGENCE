import pytest
from app.services.plan_service import PlanService

def test_generate_memorization_plan():
    service = PlanService()
    plan = service.generate_plan(
        student_level='beginner',
        duration_weeks=12,
        daily_time=30
    )
    assert 'schedule' in plan
    assert 'total_verses' in plan
    assert len(plan['schedule']) > 0

def test_calculate_daily_verses():
    service = PlanService()
    daily_verses = service.calculate_daily_verses(
        student_level='intermediate',
        daily_time=45
    )
    assert daily_verses > 0
    assert isinstance(daily_verses, int)

def test_adjust_plan_difficulty():
    service = PlanService()
    adjusted_plan = service.adjust_plan_difficulty(
        student_level='beginner',
        original_plan={'schedule': [], 'total_verses': 10}
    )
    assert 'schedule' in adjusted_plan
    assert 'difficulty_level' in adjusted_plan