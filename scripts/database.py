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
        eventbrite_url TEXT NOT NULL,
        pitchload_id TEXT,  -- Neu: ID für Pitchload-Referenz
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Table: scraped_event_ids
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scraped_event_ids (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT UNIQUE NOT NULL,
        organizer_id INTEGER NOT NULL,
        scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        processed BOOLEAN DEFAULT 0,
        FOREIGN KEY (organizer_id) REFERENCES organizers(id)
    );
    """)

    # Table: events
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT UNIQUE NOT NULL,
        organizer_id INTEGER NOT NULL,
        title TEXT,
        date TEXT,
        start_time TEXT,
        end_time TEXT,
        summary TEXT,
        description TEXT,
        ticket_url TEXT,
        is_free BOOLEAN,
        host_id TEXT,
        host_name TEXT,
        address_street TEXT,
        address_street_number TEXT,
        address_postal_code TEXT,
        address_city TEXT,
        address_state TEXT,
        address_venue_name TEXT,
        latitude REAL,
        longitude REAL,
        categories TEXT,        -- z.B. "Tech,Networking,Startup"
        target_groups TEXT,     -- z.B. "Studierende,Gründer,Investoren"
        status TEXT DEFAULT 'scraped',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (organizer_id) REFERENCES organizers(id)
    );
    """)

    # Add indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_event_id ON scraped_event_ids (event_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_organizer_id ON events (organizer_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pitchload_id ON organizers (pitchload_id);")

    conn.commit()
    conn.close()
    print("✅ Database tables successfully created or updated.")


if __name__ == "__main__":
    create_database()