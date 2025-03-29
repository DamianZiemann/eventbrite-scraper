import sqlite3

# Database file path
DATABASE = "backend/eventbrite_scraper.db"

def clean_columns():
    """Clean the target_groups and categories columns by replacing empty strings with NULL."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Update query to set NULL where columns are empty strings
    query = """
        UPDATE full_events
        SET target_groups = NULLIF(target_groups, ''),
            categories = NULLIF(categories, '')
    """
    try:
        cursor.execute(query)
        conn.commit()
        print("✅ Cleaned target_groups and categories columns successfully.")
    except sqlite3.Error as e:
        print(f"❌ Error cleaning columns: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    clean_columns()