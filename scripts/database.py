import sqlite3

# Name of the SQLite database file
DB_NAME = "backend/eventbrite_scraper.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table: organizers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS organizers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        pitchload_id TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Table: eventbrite_ids
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventbrite_ids (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        eventbrite_id TEXT NOT NULL,
        organizer_id INTEGER NOT NULL,
        scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'scraped',
        UNIQUE(eventbrite_id, organizer_id),
        FOREIGN KEY (organizer_id) REFERENCES organizers(id)
    );
    """)

    # Table: full_events
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS full_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT UNIQUE NOT NULL,
        organizer_id INTEGER,
        title TEXT,
        date TEXT,
        start TEXT,
        end TEXT,
        summary TEXT,
        description TEXT,
        ticket_url TEXT,
        free_event BOOLEAN,
        categories TEXT,
        target_groups TEXT,
        host_id TEXT,
        host_name TEXT,
        address_street TEXT,
        address_street_number TEXT,
        address_postal_code TEXT,
        address_city TEXT,
        address_state TEXT,
        address_venue_name TEXT,
        status TEXT DEFAULT 'copied',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (organizer_id) REFERENCES organizers(id)
    );
    """)

    # Add indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_eventbrite_id ON eventbrite_ids (eventbrite_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_organizer_id ON full_events (organizer_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pitchload_id ON organizers (pitchload_id);")

    conn.commit()
    conn.close()
    print("✅ Database tables successfully created or updated.")


if __name__ == "__main__":
    create_database()