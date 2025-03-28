import requests
import json
import os
import sqlite3
import time
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
EVENTBRITE_API_KEY = os.getenv("EVENTBRITE_API_KEY")
DATABASE = "backend/eventbrite_scraper.db"

# Logging configuration
def log(message, level="INFO"):
    """Custom logging function for better readability."""
    print(f"[{level}] {time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")

# Database Functions
def get_event_ids_from_db():
    """Fetch all unique event IDs and their organizer IDs from the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT eventbrite_id, organizer_id FROM eventbrite_ids")
    event_ids = cursor.fetchall()
    conn.close()
    return event_ids

def get_pitchload_id(organizer_id):
    """Fetch the pitchload_id for a given organizer_id."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT pitchload_id FROM organizers WHERE id = ?", (organizer_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# API Fetch Functions
def fetch_event_data(event_id):
    """Fetch event data from the Eventbrite API for a given event ID."""
    url = f"https://www.eventbriteapi.com/v3/events/{event_id}/"
    headers = {
        "Authorization": f"Bearer {EVENTBRITE_API_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        log(f"Failed to fetch data for event ID {event_id}: {response.status_code}", level="ERROR")
        return None

def fetch_venue_data(venue_id):
    """Fetch venue data from the Eventbrite API for a given venue ID."""
    url = f"https://www.eventbriteapi.com/v3/venues/{venue_id}/"
    headers = {
        "Authorization": f"Bearer {EVENTBRITE_API_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        log(f"Failed to fetch venue data for venue ID {venue_id}: {response.status_code}", level="ERROR")
        return None

def fetch_category_data(category_id):
    """Fetch category data from the Eventbrite API for a given category ID."""
    url = f"https://www.eventbriteapi.com/v3/categories/{category_id}/"
    headers = {
        "Authorization": f"Bearer {EVENTBRITE_API_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        log(f"Failed to fetch category data for category ID {category_id}: {response.status_code}", level="ERROR")
        return None

# Utility Functions
def split_address(address):
    """Split an address into street and street number."""
    if not address:
        return None, None
    match = re.match(r"^(.*?)(\s+\d+\w*)$", address.strip())
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return address, None

# Insert Data into Database
def insert_full_event(event_data, organizer_id):
    """Insert event data into the full_events table."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Extract and transform data
    event_id = event_data.get("id")
    title = event_data.get("name", {}).get("text")
    date = event_data.get("start", {}).get("local", "").split("T")[0]
    start = event_data.get("start", {}).get("local", "").split("T")[1] if "T" in event_data.get("start", {}).get("local", "") else None
    end = event_data.get("end", {}).get("local", "").split("T")[1] if "T" in event_data.get("end", {}).get("local", "") else None
    summary = event_data.get("summary")
    description = event_data.get("description", {}).get("text")
    ticket_url = event_data.get("url")
    free_event = event_data.get("is_free")
    category_id = event_data.get("category_id")
    venue_id = event_data.get("venue_id")
    host_id = get_pitchload_id(organizer_id)  # Fetch the pitchload_id
    host_name = event_data.get("organizer", {}).get("name")

    # Fetch additional data
    venue_data = fetch_venue_data(venue_id) if venue_id else {}
    category_data = fetch_category_data(category_id) if category_id else {}

    # Extract venue details
    full_address = venue_data.get("address", {}).get("address_1")
    address_street, address_street_number = split_address(full_address)
    address_postal_code = venue_data.get("address", {}).get("postal_code")
    address_city = venue_data.get("address", {}).get("city")
    address_state = venue_data.get("address", {}).get("region")
    address_venue_name = venue_data.get("name")

    # Extract category details
    categories = category_data.get("name")

    try:
        cursor.execute("""
            INSERT OR IGNORE INTO full_events (
                event_id, organizer_id, title, date, start, end, summary, description,
                ticket_url, free_event, categories, target_groups, host_id, host_name,
                address_street, address_street_number, address_postal_code, address_city,
                address_state, address_venue_name, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event_id, organizer_id, title, date, start, end, summary, description,
            ticket_url, free_event, categories, None, host_id, host_name,
            address_street, address_street_number, address_postal_code, address_city,
            address_state, address_venue_name, "copied"
        ))
        conn.commit()
        log(f"Inserted event ID {event_id} into full_events table.")
    except sqlite3.Error as e:
        log(f"Error inserting event ID {event_id}: {e}", level="ERROR")
    finally:
        conn.close()

# Main Function
def main():
    """Fetch and store event data for all event IDs in the database."""
    event_ids = get_event_ids_from_db()
    if not event_ids:
        log("No event IDs found in the database.", level="WARNING")
        return

    log(f"Found {len(event_ids)} event IDs in the database.")
    for event_id, organizer_id in event_ids:
        log(f"Fetching data for event ID: {event_id}")
        event_data = fetch_event_data(event_id)
        if event_data:
            insert_full_event(event_data, organizer_id)
        time.sleep(1)  # Add a 1-second delay between requests

if __name__ == "__main__":
    main()