import pytest
from backend.eventbrite_scraper import scrape_event_ids  # Importiert den Scraper

def test_scrape_event_ids():
    """Test: Überprüft, ob die Funktion Event-IDs extrahiert"""
    
    event_ids = scrape_event_ids()  # Ruft den Scraper auf

    assert len(event_ids) > 0, "❌ Es wurden keine Event-IDs gefunden!"

    print("✅ Gefundene Event-IDs:", event_ids)