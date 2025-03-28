import sqlite3

DATABASE = "backend/eventbrite_scraper.db"

def insert_organizers():
    """Insert organizer data into the organizers table."""
    organizers = [
        ("Campus Founders", "bece88f1-f96c-4b92-9375-881edba32ba9", "https://www.eventbrite.de/o/campus-founders-20213226019"),
        ("START Chapter Stuttgart", "39dff8fc-b22f-4ad0-98dc-8220c5d4051c", "https://www.eventbrite.de/o/start-chapter-stuttgart-59862120993"),
        ("KIT Gründerschmiede", "872061a2-e774-41ab-9daa-4da54dbf7f9c", "https://www.eventbrite.com/o/kit-grunderschmiede-73131571463"),
        ("Impact Hub Stuttgart", "28b634c8-4bd6-43c5-a0a6-6995d4af956f", "https://www.eventbrite.com/o/impact-hub-stuttgart-61232829253"),
        ("GRÜNDES Hochschule Esslingen", "8b8330b2-5a6b-40c0-9978-2a9a87a16a71", "https://www.eventbrite.de/o/grundes-hochschule-esslingen-18867790438")
    ]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    for name, pitchload_id, url in organizers:
        try:
            cursor.execute("""
                INSERT INTO organizers (name, pitchload_id, url)
                VALUES (?, ?, ?)
            """, (name, pitchload_id, url))
            print(f"Inserted organizer: {name}")
        except sqlite3.IntegrityError as e:
            print(f"Error inserting organizer {name}: {e}")

    conn.commit()
    conn.close()
    print("✅ All organizers have been inserted.")

if __name__ == "__main__":
    insert_organizers()