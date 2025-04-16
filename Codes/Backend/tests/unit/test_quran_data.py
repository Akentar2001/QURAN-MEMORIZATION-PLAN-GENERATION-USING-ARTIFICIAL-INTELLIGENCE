import pytest
from app.services import QuranDataService

def test_surah_data_loading():
    service = QuranDataService()
    surahs = service.get_all_surahs()
    assert len(surahs) > 0
    assert 'surah_number' in surahs[0]
    assert 'name' in surahs[0]

def test_verse_retrieval():
    service = QuranDataService()
    verses = service.get_verses_by_surah(1)
    assert len(verses) == 7  # Al-Fatiha has 7 verses