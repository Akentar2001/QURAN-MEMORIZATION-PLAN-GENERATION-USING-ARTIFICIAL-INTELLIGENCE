from app.models import verses, db
from sqlalchemy import asc, desc

class VersesService:
    @staticmethod
    def get_verse_by_id(verse_id):
        """Get verse by its ID"""
        return verses.query.get(verse_id)

    @staticmethod
    def get_verse_by_surah_and_verse(surah_id, order_in_surah):
        """Get verse by surah ID and order in surah"""
        return verses.query.filter_by(
            surah_id=surah_id, 
            order_in_surah=order_in_surah
        ).first()

    @staticmethod
    def get_next_verse(current_verse, direction=True):
        """
        Get next verse based on direction
        Args:
            current_verse: Current verse object
            direction: True for forward (order_in_quraan), False for reverse
        """
        if not current_verse:
            return None
            
        if direction:
            return verses.query.filter(
                verses.order_in_quraan == current_verse.order_in_quraan + 1
            ).first()
        else:
            return verses.query.filter(
                verses.reverse_index == current_verse.reverse_index + 1
            ).first()

    @staticmethod
    def get_verse_by_index(index, direction=True):
        """
        Get verse by its index
        Args:
            index: Index value (order_in_quraan value or reverse_index value)
            direction: True for order_in_quraan, False for reverse_index
        """
        if direction:
            return verses.query.filter(verses.order_in_quraan == index).first()
        return verses.query.filter(verses.reverse_index == index).first()

    @staticmethod
    def get_first_verse(direction=True):
        """Get first verse in Quran based on direction"""
        if direction:
            return verses.query.order_by(asc(verses.order_in_quraan)).first() #1
        return verses.query.order_by(asc(verses.reverse_index)).first() #6231