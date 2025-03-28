from __future__ import print_function
import os
from pprint import pprint
from dotenv import load_dotenv
import openapi_client
from openapi_client.rest import ApiException

# Explicitly load the .env file from the backend folder
load_dotenv(os.path.join(os.path.dirname(__file__), "../backend/.env"))

# Configure Bearer access token for authorization: bearerAuth
PITCHLOAD_API_KEY = os.getenv("PITCHLOAD_API_KEY")
if not PITCHLOAD_API_KEY:
    raise ValueError("PITCHLOAD_API_KEY is missing in the .env file.")

# Set the access token in the OpenAPI client configuration
configuration = openapi_client.Configuration()
configuration.access_token = PITCHLOAD_API_KEY

# Create an instance of the API class
api_instance = openapi_client.DefaultApi(openapi_client.ApiClient(configuration))

# Prepare the test event data
eventCreationData = {
    "title": "Test Event",
    "date": "2025-04-01",  # Example date
    "start": "2025-04-01T10:00:00",  # Example start time
    "end": "2025-04-01T12:00:00",  # Example end time
    "summary": "This is a test event for the Pitchload platform.",
    "description": "Detailed description of the test event.",
    "ticket_url": "https://example.com/tickets",
    "free_event": True,
    "categories": ["WORKSHOP_LEARNING"],  # Example category
    "target_groups": ["STUDENTS", "FOUNDERS"],  # Example target groups
    "host": {
        "host_id": "39dff8fc-b22f-4ad0-98dc-8220c5d4051c",  # Provided host_id
        "host_name": None,
        "address": {
            "street": "Test Street",
            "street_number": "123",
            "postal_code": "12345",
            "city": "Test City",
            "state": "Test State",
            "venue_name": "Test Venue"
        }
    }
}

try:
    # Create a new event
    print("Sending event creation request...")
    api_response = api_instance.post_event(eventCreationData=eventCreationData)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->post_event: %s\n" % e)