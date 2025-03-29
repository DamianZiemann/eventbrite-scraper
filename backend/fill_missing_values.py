import os
import sqlite3
from dotenv import load_dotenv
import openai

# Load environment variables from .env
load_dotenv(os.path.join(os.path.dirname(__file__), "../backend/.env"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing in the .env file.")

# Configure OpenAI API
openai.api_key = OPENAI_API_KEY

# Database file path
DATABASE = os.path.join(os.path.dirname(__file__), "../backend/eventbrite_scraper.db")

# Valid values for target_groups and categories
VALID_TARGET_GROUPS = [
    "CORPORATES", "FOUNDERS", "FOUNDERS_TO_BE", "INNOVATION_HUBS", "INVESTORS",
    "MENTORS", "PUBLIC_INSTITUTIONS", "SMALL_AND_MEDIUM_BUSINESSES", "STUDENTS"
]
VALID_CATEGORIES = [
    "COFOUNDER_MATCHING", "CONFERENCE", "DEMO_DAY", "FUNDRAISING", "JOB_FAIR",
    "NETWORKING", "PITCH", "WORKSHOP_LEARNING"
]

def get_rows_with_missing_values():
    """Fetch rows with missing target_groups or categories from the full_events table."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = """
        SELECT id, title, summary, description
        FROM full_events
        WHERE target_groups IS NULL OR categories IS NULL
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def generate_missing_values(title, summary, description):
    """Use OpenAI's GPT to generate missing target_groups and categories."""
    prompt = f"""
    The following event has missing information. Please suggest appropriate target groups and categories based on the event details:
    
    Title: {title}
    Summary: {summary or "N/A"}
    Description: {description or "N/A"}
    
    Only use the following valid values:
    - Target Groups: {", ".join(VALID_TARGET_GROUPS)}
    - Categories: {", ".join(VALID_CATEGORIES)}
    
    Provide a JSON object with two fields:
    - target_groups: a list of valid target groups
    - categories: a list of valid categories
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that generates valid target groups and categories for events."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        # Extract the content from the response
        generated_data = response['choices'][0]['message']['content']
        return eval(generated_data)  # Convert the JSON string to a Python dictionary
    except Exception as e:
        print(f"Error generating missing values: {e}")
        return {"target_groups": [], "categories": []}

def update_row_in_database(row_id, target_groups, categories):
    """Update a row in the full_events table with generated target_groups, categories, and status."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = """
        UPDATE full_events
        SET target_groups = ?, categories = ?, status = ?
        WHERE id = ?
    """
    # Handle empty values by setting them to NULL
    target_groups_value = ",".join(target_groups) if target_groups else None
    categories_value = ",".join(categories) if categories else None
    status = "LLM_FILLED"  # Set the status to indicate the values were filled by the LLM

    cursor.execute(query, (target_groups_value, categories_value, status, row_id))
    conn.commit()
    conn.close()

def fill_missing_values():
    """Main function to fill missing values in the full_events table."""
    rows = get_rows_with_missing_values()
    for row in rows:
        row_id, title, summary, description = row
        print(f"Processing row ID: {row_id}")
        
        # Generate missing values using OpenAI
        generated_data = generate_missing_values(title, summary, description)
        
        # Validate and filter the generated data
        target_groups = [tg for tg in generated_data.get("target_groups", []) if tg in VALID_TARGET_GROUPS]
        categories = [cat for cat in generated_data.get("categories", []) if cat in VALID_CATEGORIES]
        
        # Update the database
        update_row_in_database(row_id, target_groups, categories)
        print(f"Updated row ID: {row_id} with target_groups: {target_groups}, categories: {categories}, and status: LLM_FILLED")

if __name__ == "__main__":
    fill_missing_values()