import requests
import sqlite3
import time
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Constants
EVENTBRITE_API_KEY = os.getenv("EVENTBRITE_API_KEY")
DATABASE = "backend/eventbrite_scraper.db"

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log(message, level="INFO"):
    """Custom logging function for better readability."""
    logging.log(getattr(logging, level), message)

# Database Functions
def get_unprocessed_event_ids():
    """Fetch all unprocessed event IDs from the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT event_id, organizer_id 
        FROM scraped_event_ids 
        WHERE processed = 0
    """)
    event_ids = cursor.fetchall()
    conn.close()
    return event_ids

def mark_event_as_processed(event_id):
    """Mark an event ID as processed in the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE scraped_event_ids 
            SET processed = 1 
            WHERE event_id = ?
        """, (event_id,))
        conn.commit()
        log(f"Marked event ID {event_id} as processed.")
    except sqlite3.Error as e:
        log(f"Error marking event ID {event_id} as processed: {e}", level="ERROR")
    finally:
        conn.close()

def insert_event_data(event_data, venue_data, organizer_id):
    """Insert event and venue data into the Events table."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Extract and transform event data
    event_id = event_data.get("id")
    title = event_data.get("name", {}).get("text")
    date = event_data.get("start", {}).get("local", "").split("T")[0]
    start_time = event_data.get("start", {}).get("local", "").split("T")[1] if "T" in event_data.get("start", {}).get("local", "") else None
    end_time = event_data.get("end", {}).get("local", "").split("T")[1] if "T" in event_data.get("end", {}).get("local", "") else None
    summary = event_data.get("summary")
    description = event_data.get("description", {}).get("text")
    ticket_url = event_data.get("url")
    is_free = event_data.get("is_free")
    host_name = event_data.get("organizer", {}).get("name")

    # Extract and transform venue data
    address_street = venue_data.get("address", {}).get("address_1") if venue_data else None
    address_postal_code = venue_data.get("address", {}).get("postal_code") if venue_data else None
    address_city = venue_data.get("address", {}).get("city") if venue_data else None
    address_state = venue_data.get("address", {}).get("region") if venue_data else None
    address_venue_name = venue_data.get("name") if venue_data else None
    latitude = venue_data.get("latitude") if venue_data else None
    longitude = venue_data.get("longitude") if venue_data else None

    try:
        cursor.execute("""
            INSERT INTO events (
                event_id, organizer_id, title, date, start_time, end_time, summary, description,
                ticket_url, is_free, address_street, address_postal_code, address_city,
                address_state, address_venue_name, latitude, longitude, host_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event_id, organizer_id, title, date, start_time, end_time, summary, description,
            ticket_url, is_free, address_street, address_postal_code, address_city,
            address_state, address_venue_name, latitude, longitude, host_name
        ))
        conn.commit()
        log(f"Inserted event ID {event_id} into Events table.")
    except sqlite3.Error as e:
        log(f"Error inserting event ID {event_id}: {e}", level="ERROR")
    finally:
        conn.close()

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
    if not venue_id:
        return None
    url = f"https://www.eventbriteapi.com/v3/venues/{venue_id}/"
    headers = {
        "Authorization": f"Bearer {EVENTBRITE_API_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        log(f"Failed to fetch data for venue ID {venue_id}: {response.status_code}", level="ERROR")
        return None

# Main Function
def main():
    """Fetch and store event and venue data for all unprocessed event IDs."""
    event_ids = get_unprocessed_event_ids()
    if not event_ids:
        log("No unprocessed event IDs found in the database.", level="WARNING")
        return

    log(f"Found {len(event_ids)} unprocessed event IDs.")
    for event_id, organizer_id in event_ids:
        log(f"Fetching data for event ID: {event_id}")
        event_data = fetch_event_data(event_id)
        if event_data:
            venue_id = event_data.get("venue_id")
            venue_data = fetch_venue_data(venue_id)
            insert_event_data(event_data, venue_data, organizer_id)
            mark_event_as_processed(event_id)
        time.sleep(1)  # Add a 1-second delay between requests

if __name__ == "__main__":
    main()