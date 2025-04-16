import pytest
from app.services.quran_service import QuranService

def test_get_surah_info():
    service = QuranService()
    surah_info = service.get_surah_info(1)
    assert surah_info is not None
    assert surah_info['name'] == 'Al-Fatiha'
    assert surah_info['verses_count'] == 7

def test_get_verses_by_range():
    service = QuranService()
    verses = service.get_verses_by_range(1, 1, 3)
    assert len(verses) == 3
    assert all('text' in verse for verse in verses)

def test_get_surah_difficulty():
    service = QuranService()
    difficulty = service.get_surah_difficulty(1)
    assert difficulty in ['easy', 'medium', 'hard']