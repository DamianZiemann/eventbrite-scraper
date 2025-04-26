import os
import sqlite3
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PITCHLOAD_API_KEY = os.getenv("PITCHLOAD_API_KEY")
if not PITCHLOAD_API_KEY:
    raise ValueError("PITCHLOAD_API_KEY is missing in the .env file")

# Constants
DATABASE = "backend/eventbrite_scraper.db"
PITCHLOAD_API_URL = "https://pitchload.net/api/v1/events/"
HEADERS = {
    "Authorization": f"Bearer {PITCHLOAD_API_KEY}",
    "Content-Type": "application/json"
}

def fetch_events_to_push():
    """Fetch events with missing host_id and their corresponding pitchload_id."""
    query = """
        SELECT e.id, e.event_id, e.title, e.date, e.start_time, e.end_time, e.summary, 
               e.description, e.ticket_url, e.is_free, e.categories, e.target_groups, 
               o.pitchload_id, o.name, e.address_street, e.address_street_number, 
               e.address_postal_code, e.address_city, e.address_state, e.address_venue_name
        FROM events e
        JOIN organizers o ON e.organizer_id = o.id
        WHERE e.host_id IS NULL
    """
    with sqlite3.connect(DATABASE) as conn:
        return conn.execute(query).fetchall()

def push_event_to_pitchload(event):
    """Send an event to the Pitchload API."""
    payload = {
        "title": event["title"],
        "start_date": event["date"],
        "end_date": event["date"],
        "start_time": event["start_time"],
        "end_time": event["end_time"],
        "summary": event["summary"],
        "description": event["description"],
        "ticket_url": event["ticket_url"],
        "free_event": bool(event["is_free"]),  # Convert to boolean
        "categories": event["categories"].split(",") if event["categories"] else [],
        "target_groups": event["target_groups"].split(",") if event["target_groups"] else [],
        "host": {
            "host_id": event["pitchload_id"],
            "host_name": event["host_name"]
        },
        "address": {
            "street": event["address_street"],
            "street_number": event["address_street_number"],
            "postal_code": event["address_postal_code"],
            "city": event["address_city"],
            "state": event["address_state"],
            "venue_name": event["address_venue_name"]
        }
    }
    try:
        response = requests.post(PITCHLOAD_API_URL, headers=HEADERS, json=payload)

        if response.status_code == 201:
            print(f"✅ Event '{event['title']}' successfully pushed to Pitchload.")
            return True
        elif "Uniqueness violation" in response.text:
            print(f"⚠️ Event '{event['title']}' already exists on Pitchload. Skipping.")
            return True  # Treat as success to avoid retrying
        else:
            print(f"❌ Failed to push event '{event['title']}': {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

def update_event_host_id(event_id, pitchload_id):
    """Update the host_id in the events table after successful push."""
    query = "UPDATE events SET host_id = ? WHERE id = ?"
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(query, (pitchload_id, event_id))
        conn.commit()

def main():
    """Main function to push events to Pitchload."""
    events = fetch_events_to_push()
    if not events:
        print("No events to push.")
        return

    for event in events:
        event_data = {
            "id": event[0],
            "event_id": event[1],
            "title": event[2],
            "date": event[3],
            "start_time": event[4],
            "end_time": event[5],
            "summary": event[6],
            "description": event[7],
            "ticket_url": event[8],
            "is_free": event[9],
            "categories": event[10],
            "target_groups": event[11],
            "pitchload_id": event[12],
            "host_name": event[13],
            "address_street": event[14],
            "address_street_number": event[15],
            "address_postal_code": event[16],
            "address_city": event[17],
            "address_state": event[18],
            "address_venue_name": event[19]
        }

        if push_event_to_pitchload(event_data):
            update_event_host_id(event_data["id"], event_data["pitchload_id"])

if __name__ == "__main__":
    main()