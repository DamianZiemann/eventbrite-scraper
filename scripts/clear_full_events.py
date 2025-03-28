import sqlite3

# Database configuration
DATABASE = "backend/eventbrite_scraper.db"

def clear_full_events_table():
    """Clear all data from the full_events table."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        # Clear the table
        cursor.execute("DELETE FROM full_events")
        conn.commit()
        print("✅ Successfully cleared the full_events table.")
    except sqlite3.Error as e:
        print(f"❌ Error clearing the full_events table: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    clear_full_events_table()