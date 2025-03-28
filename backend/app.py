from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import validators

# Initialize Flask application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "DELETE"])  # Enable CORS for frontend communication

# Database file path
DATABASE = os.path.join(os.path.dirname(__file__), "eventbrite_scraper.db")
print("📦 Current database file:", os.path.abspath(DATABASE))

def get_db_connection():
    """Helper function to get a database connection with foreign key support."""
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200

@app.route("/organizers", methods=["POST"])
def add_organizer():
    """Add a new organizer."""
    try:
        data = request.get_json()
        name = data.get("name")
        url = data.get("url")

        if not name or not url:
            return jsonify({"error": "Name or URL is missing"}), 400

        if not validators.url(url):
            return jsonify({"error": "Invalid URL"}), 400

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO organizers (name, url) VALUES (?, ?)", (name, url))
            conn.commit()
        return jsonify({"message": "Organizer added successfully"}), 201
    except Exception as e:
        print("Error while adding organizer:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/organizers", methods=["GET"])
def get_organizers():
    """Get all organizers."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT organizers.id, organizers.name, organizers.url, 
                       COUNT(eventbrite_ids.id) AS event_count
                FROM organizers
                LEFT JOIN eventbrite_ids ON organizers.id = eventbrite_ids.organizer_id
                GROUP BY organizers.id
            """
            cursor.execute(query)
            data = cursor.fetchall()
        return jsonify([
            {"id": row[0], "name": row[1], "url": row[2], "event_count": row[3]} for row in data
        ])
    except Exception as e:
        print("Error while fetching organizers:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/organizers/<int:organizer_id>", methods=["DELETE"])
def delete_organizer(organizer_id):
    """Delete an organizer."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM eventbrite_ids WHERE organizer_id = ?", (organizer_id,))
            event_count = cursor.fetchone()[0]

            if event_count > 0:
                return jsonify({"error": "Organizer cannot be deleted because there are associated events."}), 400

            cursor.execute("DELETE FROM organizers WHERE id = ?", (organizer_id,))
            conn.commit()
        return "", 204
    except sqlite3.Error as e:
        print(f"Database error while deleting organizer {organizer_id}: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route("/organizers/<int:organizer_id>/events", methods=["GET"])
def get_events_for_organizer(organizer_id):
    """Get events for a specific organizer."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT event_id, title, date, start, end, description, ticket_url, 
                       address_street, address_street_number, address_city
                FROM full_events
                WHERE organizer_id = ?
            """
            cursor.execute(query, (organizer_id,))
            events = cursor.fetchall()
        return jsonify([
            {
                "event_id": row[0],
                "title": row[1],
                "date": row[2],
                "start": row[3],
                "end": row[4],
                "description": row[5],
                "ticket_url": row[6],
                "address_street": row[7],
                "address_street_number": row[8],
                "address_city": row[9],
            } for row in events
        ])
    except Exception as e:
        print(f"Error fetching events for organizer {organizer_id}: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)