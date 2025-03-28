import pytest
import os
from dotenv import load_dotenv

def test_eventbrite_api_key_exists():
    """Test: Überprüft, ob der API-Key vorhanden ist"""

    load_dotenv
    
    eventbrite_API = os.getenv("EVENTBRITE_API_KEY")  

    assert eventbrite_API is None and eventbrite_API != "", "EVENTBRITE_API_KEY ist nicht gesetzt"