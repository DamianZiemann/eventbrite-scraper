import sqlite3
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# Database configuration
DATABASE = "backend/eventbrite_scraper.db"

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_organizer_links():
    """Fetch organizer URLs and IDs from the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, url FROM organizers")
    organizers = cursor.fetchall()
    conn.close()
    return organizers

def insert_event_ids(event_ids, organizer_id):
    """Insert event IDs into the database, ensuring no duplicates."""
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    for event_id in event_ids:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO eventbrite_ids (eventbrite_id, organizer_id) 
                VALUES (?, ?)
            """, (event_id, organizer_id))
        except sqlite3.Error as e:
            logging.error(f"Error inserting event ID {event_id} for organizer ID {organizer_id}: {e}")
    conn.commit()
    conn.close()

def scrape_event_ids(url):
    """Scrape unique event IDs from an Eventbrite organizer page, including pagination."""
    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    event_ids = set()  # Use a set to store unique event IDs

    try:
        driver.get(url)
        logging.info(f"Accessing URL: {url}")

        while True:
            try:
                # Wait for event links to load
                WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "event-card-link"))
                )

                # Extract event IDs from the current page
                event_links = driver.find_elements(By.CLASS_NAME, "event-card-link")
                logging.info(f"Found {len(event_links)} event links on the current page.")

                for link in event_links:
                    href = link.get_attribute("href")
                    if href and "tickets-" in href:
                        event_id = href.split("tickets-")[-1].split("?")[0]
                        if event_id.isdigit() and len(event_id) == 13:  # Validate event ID length
                            event_ids.add(event_id)

                # Check for the "Next" button and navigate to the next page
                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(@aria-label, 'Next')]"))
                    )
                    if "disabled" in next_button.get_attribute("class"):
                        logging.info("No more pages found. Scraping complete for this organizer.")
                        break
                    logging.info("Navigating to the next page...")
                    next_button.click()
                    sleep(5)  # Wait for the next page to load
                except Exception:
                    logging.info("No more pages found. Scraping complete for this organizer.")
                    break

            except Exception as e:
                logging.error(f"Error while scraping events from {url}: {e}")
                break
    finally:
        driver.quit()

    return event_ids

def scrape_and_show_event_ids():
    """Scrape and display unique event IDs for all organizers in the database."""
    organizers = get_organizer_links()

    if not organizers:
        logging.info("No organizers found in the database.")
        return

    for organizer_id, organizer_url in organizers:
        logging.info(f"Scraping events for organizer ID {organizer_id}, URL: {organizer_url}")
        
        # Scrape event IDs for the current organizer
        event_ids = scrape_event_ids(organizer_url)
        logging.info(f"Found {len(event_ids)} unique event IDs for organizer ID {organizer_id}.")

        # Insert the scraped event IDs into the database
        insert_event_ids(event_ids, organizer_id)

        # Display the scraped event IDs in the terminal
        print(f"\nOrganizer ID: {organizer_id}")
        print(f"Scraped {len(event_ids)} event IDs:")
        for event_id in sorted(event_ids):
            print(f"- {event_id}")
        print("-" * 50)

if __name__ == "__main__":
    scrape_and_show_event_ids()